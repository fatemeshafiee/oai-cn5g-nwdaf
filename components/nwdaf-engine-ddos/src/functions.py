#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this
# * file except in compliance with the License. You may obtain a copy of the
# * License at
# *
# *      http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *      contact@openairinterface.org
# */

#/*
# * Author: Abdelkader Mekrache <mekrache@eurecom.fr>
# * Description: This file contains utils functions.
# */
import logging
import pandas as pd
from src.config import *
import base64
import ipaddress
import struct
from sklearn.preprocessing import StandardScaler

def add_time_columns(df, timestamp_col):
    df['timestamp'] = pd.to_datetime(df[timestamp_col], unit='s')
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    return df
#[FATEMEH]: Change to get the related data from packets
#features=[ 'Dst IP','Dst Port', 'Fwd Pkt Len Std','Src IP',
#         'Src Port', 'ACK Flag Cnt', 'Protocol','Tot Fwd Pkts',
#         'Fwd Seg Size Min','Slice']

def pre_process(raw_data):
    data = []
    for entry in raw_data:
        processed_entry = {}
        #check if the transport packet is tcp
        packet_data =  base64.b64decode(entry["data"])
        if int(entry["protocol"]) == 6:
            tcp_header = packet_data[20:40]
            src_port, dst_port, seq_num, ack_num, offset_reserved, flags, window, checksum, urgent_pointer = struct.unpack("!HHLLBBHHH", tcp_header)

            data_offset = (offset_reserved >> 4) * 4
            reserved = offset_reserved & 0x0F

            # Extract the TCP flags
            fin = (flags & 0x01) != 0
            syn = (flags & 0x02) != 0
            rst = (flags & 0x04) != 0
            psh = (flags & 0x08) != 0
            ack = (flags & 0x10) != 0
            urg = (flags & 0x20) != 0
            ece = (flags & 0x40) != 0
            cwr = (flags & 0x80) != 0
            processed_entry["Dst_IP"] = entry["IPdst"]
            processed_entry["Dst_Port"] = dst_port
            processed_entry["Fwd_Pkt_Len"] = int(entry["packetlength"])
            processed_entry["Src_IP"] = entry["IPsrc"]
            processed_entry["Src_Port"] = src_port
            processed_entry["ACK_Flag"] = int(ack)
            processed_entry["Protocol"] = int(entry["protocol"])
            processed_entry["Fwd_Seg_Size"] = int(entry["datalength"])
            processed_entry["Slice"] = 0
            processed_entry["timestamp"] = entry["timestamp"]
            processed_entry["pduseid"] = entry["pduseid"]
            processed_entry["seid"] = entry["seid"]
            data.append(processed_entry)
        if int(entry["protocol"]) == 17:
            udp_header = packet_data[20:28]  # UDP header is always 8 bytes

            # Unpack the UDP header fields
            src_port, dst_port, length, checksum = struct.unpack("!HHHH", udp_header)
            processed_entry["Dst_IP"] = entry["IPdst"]
            processed_entry["Dst_Port"] = dst_port
            processed_entry["Fwd_Pkt_Len"] = int(entry["packetlength"])
            processed_entry["Src_IP"] = entry["IPsrc"]
            processed_entry["Src_Port"] = src_port
            processed_entry["ACK_Flag"] = 0
            processed_entry["Protocol"] = int(entry["protocol"])
            processed_entry["Fwd_Seg_Size"] = int(entry["datalength"])
            processed_entry["Slice"] = 0
            processed_entry["timestamp"] = entry["timestamp"]
            processed_entry["pduseid"] = entry["pduseid"]
            processed_entry["seid"] = entry["seid"]

            data.append(processed_entry)
    return data



def create_dataframe():
    raw_data = []
    for doc in smf_collection.find():
        if "packet_list" not in doc:
            continue
        for packet in doc['packet_list']:
            raw_data.append({
                "timestamp": packet['timestamp'],
                "pduseid": packet['pduseid'],
                "seid": packet['packetinfo']['seid'],
                "datalength": packet['packetinfo']['packetdata']['datalength'],
                "data": packet['packetinfo']['packetdata']['data'],
                "datalength": packet['packetinfo']['packetdata']['datalength'],
                "data": packet['packetinfo']['packetdata']['data'],
                "protocol": packet['packetinfo']['packetheader']['protocol'],
                "IPsrc": packet['packetinfo']['packetheader']['src'],
                "IPdst": packet['packetinfo']['packetheader']['dst'],
                "checksum": packet['packetinfo']['packetheader']['checksum'],
                "ttl": packet['packetinfo']['packetheader']['ttl'],
                "flags": packet['packetinfo']['packetheader']['flags'],
                "fragid": packet['packetinfo']['packetheader']['fragid'],
                "tos": packet['packetinfo']['packetheader']['tos'],
                "packetlength": packet['packetinfo']['packetheader']['packetlength'],

            })

    # Create a pandas dataframe
    data = pre_process(raw_data)
    df = pd.DataFrame(data)
    # df = add_time_columns(df, 'timestamp')
    result_df = create_flow(df)
    return result_df

def create_flow(df):
    logging.info("The df is ", df)

    result_df = df.groupby(["Dst_IP", "Dst_Port", "Src_IP", "Src_Port", "Protocol", "pduseid", "seid"]).agg(
        Fwd_Pkt_Len_Std=("Fwd_Pkt_Len", "std"),
        ACK_Flag_Count=("ACK_Flag", "sum"),
        Tot_Fwd_Pkts=("Src_IP", "count"),
        Flow_duration=("timestamp", lambda x: x.max() - x.min()),
        Fwd_Seg_Size_Min=("Fwd_Seg_Size", "min")
    ).reset_index()

    result_df["Slice"] = 0  # Add a placeholder 'Slice' column with a default value of 0

    result_df = result_df[["Flow_duration","Dst_IP", "Dst_Port", "Fwd_Pkt_Len_Std", "Src_IP", "Src_Port",
                           "ACK_Flag_Count", "Protocol", "Tot_Fwd_Pkts", "Fwd_Seg_Size_Min","Slice", "pduseid", "seid"]]
    result_df = result_df.rename(columns={
        "Flow_Duration": "Flow Duration",
        "Dst_IP": "Dst IP",
        "Dst_Port": "Dst Port",
        "Fwd_Pkt_Len_Std": "Fwd Pkt Len Std",
        "Src_IP": "Src IP",
        "Src_Port": "Src Port",
        "ACK_Flag_Count": "ACK Flag Cnt",
        "Protocol": "Protocol",
        "Tot_Fwd_Pkts": "Tot Fwd Pkts",
        "Fwd_Seg_Size_Min": "Fwd Seg Size Min",
        "Slice": "Slice",
        "pduseid": "pduseid",
        "seid": "seid"
    })


    return result_df


#[FATEMEH]: Change to get the related data from packets
#features=[ 'Dst IP','Dst Port', 'Fwd Pkt Len Std','Src IP',
#         'Src Port', 'ACK Flag Cnt', 'Protocol','Tot Fwd Pkts',
#         'Fwd Seg Size Min','Slice']
