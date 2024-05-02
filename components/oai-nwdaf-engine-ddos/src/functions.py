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

import pandas as pd
from src.config import *
import base64
import ipaddress



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
            processed_entry["Dst IP"] = entry["IPdst"]
            processed_entry["Dst Port"] = dst_port
            processed_entry["Fwd Pkt Len"] = int(entry["packetlength"])
            processed_entry["Src IP"] = entry["IPsrc"]
            processed_entry["Src Port"] = src_port
            processed_entry["ACK Flag"] = int(ack)
            processed_entry["Protocol"] = int(entry["protocol"])
            processed_entry["Fwd Seg Size"] = int(entry["datalength"])
            processed_entry["Slice"] = 0
            processed_entry["timestamp"] = entry["timestamp"]
            data.append(processed_entry)
        if int(entry["protocol"]) == 17:
            udp_header = packet_data[20:28]  # UDP header is always 8 bytes

            # Unpack the UDP header fields
            src_port, dst_port, length, checksum = struct.unpack("!HHHH", udp_header)
            processed_entry["Dst IP"] = entry["IPdst"]
            processed_entry["Dst Port"] = dst_port
            processed_entry["Fwd Pkt Len"] = int(entry["packetlength"])
            processed_entry["Src IP"] = entry["IPsrc"]
            processed_entry["Src Port"] = src_port
            processed_entry["Protocol"] = int(entry["protocol"])
            processed_entry["Fwd Seg Size"] = int(entry["datalength"])
            processed_entry["Slice"] = 0
            processed_entry["timestamp"] = entry["timestamp"]

            data.append(processed_entry)
    return data



def create_dataframe():
    raw_data = []
    for doc in smf_collection.find():
        for packet in doc['packet_list']:
            raw_data.append({
                "timestamp": packet['timestamp'],
                "pduseid": packet['pduseid'],
                "datalength": packet['packetdata']['datalength'],
                "data": packet['packetdata']['data'],
                "pduseid": packet['pduseid'],
                "datalength": packet['packetdata']['datalength'],
                "data": packet['packetdata']['data'],
                "protocol": packet['packetheader']['protocol'],
                "IPsrc": packet['packetheader']['src'],
                "IPdst": packet['packetheader']['dst'],
                "checksum": packet['packetheader']['checksum'],
                "ttl": packet['packetheader']['ttl'],
                "flags": packet['packetheader']['flags'],
                "fragid": packet['packetheader']['fragid'],
                "tos": packet['packetheader']['tos'],
                "packetlength": packet['packetheader']['packetlength'],

            })

    # Create a pandas dataframe
    data = pre_process(raw_data)
    df = pd.DataFrame(data)
    df = add_time_columns(df, 'timestamp')
    return df

def create_flow(df):
    result_df = df.groupby(["Dst IP", "Dst Port", "Src IP", "Src Port", "Protocol"]).agg(
        Fwd_Pkt_Len_Std=("Fwd Pkt Len", "std"),
        ACK_Flag_Count=("ACK Flag", "sum"),
        Tot_Fwd_Pkts=("Src IP", "count"),
        Flow_duration=("Timestamp", lambda x: x.max() - x.min()),
        Fwd_Seg_Size_Min=("Fwd Seg Size", "min")
    ).reset_index()

    result_df["Slice"] = 0  # Add a placeholder 'Slice' column with a default value of 0

    result_df = result_df[["Dst IP", "Dst Port", "Fwd_Pkt_Len_Std", "Src IP", "Src Port",
                           "ACK_Flag_Count", "Protocol", "Tot_Fwd_Pkts", "Fwd_Seg_Size_Min", "Slice"]]

    return result_df


