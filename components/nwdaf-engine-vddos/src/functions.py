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
# * Author: Fatemeh Shafiei Ardestani
# * Description: This file contains utils functions.
# */

import pandas as pd
import logging
from src.config import *
import json
import ipaddress

def add_time_columns(df, timestamp_col):
    df['timestamp'] = pd.to_datetime(df[timestamp_col], unit='s')
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    return df


def extract_flow_info(flowDescription):

    flowDescription = flowDescription.replace('\n', '').replace('+', '')
    flow_json = json.loads(flowDescription)
    seID = flow_json.get('SeId')
    SrcIp = flow_json.get('SrcIp')
    DstIp = flow_json.get('DstIp')
    SrcPort = flow_json.get('SrcPort')
    DstPort = flow_json.get('DstPort')

    return seID, SrcIp, DstIp, SrcPort, DstPort

def ip_to_int(ip_str):
    if ipaddress.ip_address(ip_str).version == 4:
        return int(ipaddress.IPv4Address(ip_str)),"IP4"
    elif ipaddress.ip_address(ip_str).version == 6:
        return int(ipaddress.IPv6Address(ip_str)),"IP6"

def create_dataframe():
    data = []

    for doc in upf_collection.find():
        for rep_per_ue in doc['upfeventexposure']:
            timestamp = rep_per_ue['timestamp']
            for user_usage in rep_per_ue['userdatausagemeasurements']:
                volume = user_usage['volumemeasurement']
                flowDescription = user_usage['flowinfo']['flowdescription']
                seID, SrcIp, DstIp, SrcPort, DstPort = extract_flow_info(flowDescription)
                src_ip_int, v = ip_to_int(SrcIp)
                dst_ip_int, v = ip_to_int(DstIp)
                if v == "IP6":
                    continue

                logging.info(f"the volume is: {volume['ulvolume']}")
                logging.info(f"the volume is: {volume['ulvolume'][:-1]}")
                ulVolume = int(volume['ulvolume'][:-1])
                dlVolume = int(volume['dlvolume'][:-1])
                totalVolume = int(volume['totalvolume'][:-1])
                ulPacket = int(volume['ulnbofpackets'])
                dlPacket = int(volume['dlnbofpackets'])
                totalPacket = int(volume['totalnbofpackets'])
                data.append({
                    "seID":int(seID),
                    "SrcIp":src_ip_int,
                    "DstIp":dst_ip_int,
                    "SrcPort":int(SrcPort),
                    "DstPort":int(DstPort),
                    "ulVolume": ulVolume, #-  lastUlVolume,
                    "dlVolume": dlVolume, #- lastDlVolume,
                    "totalVolume": totalVolume, #- lastTotalVolume,
                    "ulPacket": ulPacket, #- lastUlPacket,
                    "dlPacket": dlPacket, #- lastDlPacket,
                    "totalPacket": totalPacket,
                     'timestamp':timestamp #- lastTotalPacket
                })
    df = pd.DataFrame(data)


    grouped_df = df.groupby(['seID', 'SrcPort', 'SrcIp', 'DstPort', 'DstIp'])
    df['ActualUlVolume'] = grouped_df['ulVolume'].diff().fillna(df['ulVolume']).astype(int)
    df['ActualDlVolume'] = grouped_df['dlVolume'].diff().fillna(df['dlVolume']).astype(int)
    df["ActualTotalVolume"] = grouped_df["totalVolume"].diff().fillna(df['totalVolume']).astype(int)
    df["ActualUlPacket"] = grouped_df["ulPacket"].diff().fillna(df["ulPacket"]).astype(int)
    df["ActualDlPacket"] = grouped_df["dlPacket"].diff().fillna(df["dlPacket"]).astype(int)
    df["ActualTotalPacket"] = grouped_df["totalPacket"].diff().fillna(df["totalPacket"]).astype(int)

    df = df.drop(columns=['ulVolume', 'dlVolume', 'totalVolume', 'ulPacket', 'dlPacket', 'totalPacket'])
#     df["flowDuration"] = grouped_df['timestamp'].transform(lambda x: x.max() - x.min())
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['UlRate'] = df['ActualUlVolume'] / df['timestamp'].diff().dt.total_seconds()
    df['DlRate'] = df['ActualDlVolume'] / df['timestamp'].diff().dt.total_seconds()
    df['UlPacketRate'] = df['ActualUlPacket'] / df['timestamp'].diff().dt.total_seconds()
    df['DlPacketRate'] = df['ActualDlPacket'] / df['timestamp'].diff().dt.total_seconds()
    df['PacketRatio'] = df['ActualUlPacket'] / (df['ActualDlPacket'] + 1)
    df['VolumeRatio'] = df['ActualUlVolume'] / (df['ActualDlVolume'] + 1)
    df['VolumeDifference'] = df['ActualUlVolume'] - df['ActualDlVolume']
    df.set_index('timestamp', inplace=True)
    grouped_df = df.groupby(['seID', 'SrcIp', 'DstIp', 'SrcPort', 'DstPort'])
    result = grouped_df.resample('75S').agg({
        'ActualUlVolume': 'sum',
        'ActualDlVolume': 'sum',
        'ActualTotalVolume' : 'sum',
        'ActualUlPacket': 'sum',
        'ActualDlPacket': 'sum',
        'ActualTotalPacket': 'sum'

    })
    result['UlRate'] = result['ActualUlVolume'] / 75  # Assuming 75 seconds between resamples
    result['DlRate'] = result['ActualDlVolume'] / 75
    result['UlPacketRate'] = result['ActualUlPacket'] / 75
    result['DlPacketRate'] = result['ActualDlPacket'] / 75
    result['PacketRatio'] = result['ActualUlPacket'] / (result['ActualDlPacket'] + 1)
    result['VolumeRatio'] = result['ActualUlVolume'] / (result['ActualDlVolume'] + 1)
    result['VolumeDifference'] = result['ActualUlVolume'] - result['ActualDlVolume']

    return df