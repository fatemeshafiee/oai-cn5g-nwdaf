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
import numpy as np
import networkx as nx

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
        for rep_per_ue in doc['upf_volume']:
            timestamp = rep_per_ue['timestamp']
            for user_usage in rep_per_ue['userdatausagemeasurements']:
                volume = user_usage['volumemeasurement']
                packfiltid = user_usage['flowinfo']['packfiltid']
                seID, SrcIp, DstIp, SrcPort, DstPort = extract_flow_info(packfiltid)
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
    return df
def src_dst_based_df(df):
        grouped_df = df.groupby(['SrcIp', 'DstIp', 'timestamp']).agg({
                                                           'ulVolume' : 'sum',
                                                           'dlVolume' : 'sum',
                                                           'totalVolume' : 'sum',
                                                           'ulPacket': 'sum',
                                                           'dlPacket': 'sum',
                                                           'totalPacket': 'sum'
                                                       }).reset_index()
        grouped_df = grouped_df.sort_values(by=['SrcIp','DstIp','timestamp'])
        grouped_df['ulVolume'] = grouped_df.groupby(['SrcIp','DstIp'])['ulVolume'].diff().fillna(grouped_df['ulVolume'])
        grouped_df['dlVolume'] = grouped_df.groupby(['SrcIp','DstIp'])['dlVolume'].diff().fillna(grouped_df['dlVolume'])
        grouped_df['totalVolume'] = grouped_df.groupby(['SrcIp','DstIp'])['totalVolume'].diff().fillna(grouped_df['totalVolume'])

        grouped_df['ulPacket'] = grouped_df.groupby(['SrcIp','DstIp'])['ulPacket'].diff().fillna(grouped_df['ulPacket'])
        grouped_df['dlPacket'] = grouped_df.groupby(['SrcIp','DstIp'])['dlPacket'].diff().fillna(grouped_df['dlPacket'])
        grouped_df['totalPacket'] = grouped_df.groupby(['SrcIp','DstIp'])['totalPacket'].diff().fillna(grouped_df['totalPacket'])
        return grouped_df

def create_ue_profile(df):
    grouped_df = df.groupby(['SrcIp', 'timestamp']).agg({
                                                       'ulVolume' : 'sum',
                                                       'dlVolume' : 'sum',
                                                       'totalVolume' : 'sum',
                                                       'ulPacket': 'sum',
                                                       'dlPacket': 'sum',
                                                       'totalPacket': 'sum'
                                                   }).reset_index()
    grouped_df = grouped_df.sort_values(by=['SrcIp', 'timestamp'])
    grouped_df['ulVolume'] = grouped_df.groupby('SrcIp')['ulVolume'].diff().fillna(grouped_df['ulVolume'])
    grouped_df['dlVolume'] = grouped_df.groupby('SrcIp')['dlVolume'].diff().fillna(grouped_df['dlVolume'])
    grouped_df['totalVolume'] = grouped_df.groupby('SrcIp')['totalVolume'].diff().fillna(grouped_df['totalVolume'])

    grouped_df['ulPacket'] = grouped_df.groupby('SrcIp')['ulPacket'].diff().fillna(grouped_df['ulPacket'])
    grouped_df['dlPacket'] = grouped_df.groupby('SrcIp')['dlPacket'].diff().fillna(grouped_df['dlPacket'])
    grouped_df['totalPacket'] = grouped_df.groupby('SrcIp')['totalPacket'].diff().fillna(grouped_df['totalPacket'])

    df = df.sort_values(by=['SrcIp', 'timestamp'])
    df['time_diff'] = df.groupby('SrcIp')['timestamp'].diff().dt.total_seconds().fillna(0)
    df['uplink_throughput'] = df['ulVolume'] / df['time_diff']
    df['downlink_throughput'] = df['dlVolume'] / df['time_diff']
    df['total_throughput'] = df['uplink_throughput'] + df['downlink_throughput']

    df['uplink_throughput'] = df['uplink_throughput'].replace([float('inf'), None], 0)
    df['downlink_throughput'] = df['downlink_throughput'].replace([float('inf'), None], 0)
    df['total_throughput'] = df['total_throughput'].replace([float('inf'), None], 0)

    avg_uplink_throughput = df['uplink_throughput'].mean()
    avg_downlink_throughput = df['downlink_throughput'].mean()
    avg_total_throughput = df['total_throughput'].mean()

    peak_uplink_throughput = df['uplink_throughput'].max()
    peak_downlink_throughput = df['downlink_throughput'].max()
    peak_total_throughput = df['total_throughput'].max()




    df['uplink_packet_rate'] = df['ulPacket'] / df['time_diff']
    df['downlink_packet_rate'] = df['dlPacket'] / df['time_diff']
    df['total_packet_rate'] = df['uplink_packet_rate'] + df['downlink_packet_rate']


    df['uplink_packet_rate'] = df['uplink_packet_rate'].replace([float('inf'), None], 0)
    df['downlink_packet_rate'] = df['downlink_packet_rate'].replace([float('inf'), None], 0)
    df['total_packet_rate'] = df['total_packet_rate'].replace([float('inf'), None], 0)

    avg_uplink_packet_rate = df['uplink_packet_rate'].mean()
    avg_downlink_packet_rate = df['downlink_packet_rate'].mean()
    avg_total_packet_rate = df['total_packet_rate'].mean()

    peak_uplink_packet_rate = df['uplink_packet_rate'].max()
    peak_downlink_packet_rate = df['downlink_packet_rate'].max()
    peak_total_packet_rate = df['total_packet_rate'].max()


    summary_per_ip = df.groupby('SrcIp').agg(
         avg_uplink_throughput=('uplink_throughput', 'mean'),
         peak_uplink_throughput=('uplink_throughput', 'max'),
         avg_downlink_throughput=('downlink_throughput', 'mean'),
         peak_downlink_throughput=('downlink_throughput', 'max'),
         avg_total_throughput=('total_throughput', 'mean'),
         peak_total_throughput=('total_throughput', 'max'),
         avg_uplink_packet_rate=('uplink_packet_rate', 'mean'),
         peak_uplink_packet_rate=('uplink_packet_rate', 'max'),
         avg_downlink_packet_rate=('downlink_packet_rate', 'mean'),
         peak_downlink_packet_rate=('downlink_packet_rate', 'max'),
         avg_total_packet_rate=('total_packet_rate', 'mean'),
         peak_total_packet_rate=('total_packet_rate', 'max')
    ).reset_index()



    return summary_per_ip

def build_graph_per_batch(df_flow):
  G = nx.DiGraph()
  for _, row in df_flow.iterrows():
    G.add_edge(row['src_ip'], row['dst_ip'], weight=row['src_pkts'])
    G.add_edge(row['dst_ip'], row['src_ip'], weight=row['dst_pkts'])
  return G
def extract_grapgh_features(G, bot_ips):
   features = []
   # print(G.in_degree())
   in_degree = dict(G.in_degree())
   out_degree = dict(G.out_degree())
   w_in_degree = dict(G.in_degree(weight='weight'))
   w_out_degree = dict(G.out_degree(weight='weight'))
   betweenness = nx.betweenness_centrality(G, weight='weight')
   lcc = compute_lcc(G)

   for node in G.nodes():
       features.append([
         node,
         in_degree.get(node, 0),
         out_degree.get(node, 0),
         w_in_degree.get(node, 0),
         w_out_degree.get(node, 0),
         betweenness.get(node, 0),
         lcc.get(node, 0.0)
     ])

   features_df = pd.DataFrame(features, columns=['host_ip',
         'in_degree', 'out_degree', 'w_in_degree', 'w_out_degree',
         'betweenness', 'LCC'
     ])
   return features_df
def create_graph_feature(benign_df):
    benign_df['timestamp'] = pd.to_datetime(benign_df['timestamp'])
    df_grouped = benign_df.groupby(['SrcIp', 'DstIp', 'timestamp']).agg({
                                                               'ulVolume' : 'sum',
                                                               'dlVolume' : 'sum',
                                                               'totalVolume' : 'sum',
                                                               'ulPacket': 'sum',
                                                               'dlPacket': 'sum',
                                                               'totalPacket': 'sum'
                                                           }).reset_index()
    df_grouped = df_grouped.sort_values(by=['SrcIp', 'DstIp', 'timestamp'])

    df_grouped['ulVolume_diff'] = df_grouped.groupby(['SrcIp', 'DstIp'])['ulVolume'].diff().fillna(df_grouped['ulVolume'])
    df_grouped['dlVolume_diff'] = df_grouped.groupby(['SrcIp', 'DstIp'])['dlVolume'].diff().fillna(df_grouped['dlVolume'])
    df_grouped['totalVolume_diff'] = df_grouped['ulVolume_diff'] + df_grouped['dlVolume_diff']


    df_grouped['ulPacket_diff'] = df_grouped.groupby(['SrcIp', 'DstIp'])['ulPacket'].diff().fillna(df_grouped['ulPacket'])
    df_grouped['dlPacket_diff'] = df_grouped.groupby(['SrcIp', 'DstIp'])['dlPacket'].diff().fillna(df_grouped['dlPacket'])
    df_grouped['totalPacket_diff'] = df_grouped['ulPacket_diff'] + df_grouped['dlPacket_diff']
    columns_to_drop = ['timestamp', 'ulVolume', 'dlVolume', 'totalVolume', 'ulPacket', 'dlPacket', 'totalPacket', 'totalVolume_diff','totalPacket_diff']
    df_grouped = df_grouped.drop(columns=columns_to_drop)
    df_grouped = df_grouped.groupby(['SrcIp', 'DstIp']).sum().reset_index()
    df_grouped = df_grouped.rename(columns={'SrcIp': 'src_ip', 'DstIp': 'dst_ip', 'ulVolume_diff':'src_size','dlVolume_diff':'dst_size', 'ulPacket_diff':'src_pkts', 'dlPacket_diff':'dst_pkts' })
    G = build_graph_per_batch(df_grouped)
    G_features = extract_grapgh_features(G, ['10.42.0.2', '10.42.0.3', '10.42.0.4', '10.42.0.5', '10.42.0.6', '10.42.0.7'])
    return G_features


