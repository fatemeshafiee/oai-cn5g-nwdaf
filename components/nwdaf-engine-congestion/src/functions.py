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
#  Author: Fatemeh Shafiei Ardestani
#  Created on: 2025-04-06
#*/
import pandas as pd
import logging
from src.config import *
import src.config as config
import json
import ipaddress
import numpy as np
import networkx as nx
import requests
from datetime import datetime, timedelta



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
    df = pd.DataFrame()
    data = []
    unique_pairs = set()
    t = 30  # number of seconds to look back
    cutoff_time = datetime.utcnow() - timedelta(seconds=t)
    if MONGODB_COLLECTION_NAME_UPF in nwdaf_db.list_collection_names():
        for doc in upf_collection.find({"timestamp": {"$gte": cutoff_time}}):
            timestamp = doc['timestamp']
            tsm = doc['throughputStatisticsMeasurement']
            seID = doc['seID']
            SrcIp = doc['SrcIp']
            DstIp = doc['DstIp']
            SrcPort = doc['SrcPort']
            DstPort = doc['DstPort']
            src_ip_int, v = ip_to_int(SrcIp)
            dst_ip_int, v = ip_to_int(DstIp)
            if v == "IP6":
                continue
            ulPeakThroughput = int(tsm['ulPeakThroughput'][:-3])
            dlPeakThroughput = int(tsm['dlPeakThroughput'][:-3])
            ulAveragePacketThroughput = int(tsm['ulAveragePacketThroughput'][:-3])
            dlAveragePacketThroughput = int(tsm['dlAveragePacketThroughput'][:-3])
            ulPeakPacketThroughput = int(tsm['ulPeakPacketThroughput'][:-3])
            dlPeakPacketThroughput = int(tsm['dlPeakPacketThroughput'][:-3])
            ulAverageThroughput = int(tsm['ulAverageThroughput'][:-3])
            dlAverageThroughput = int(tsm['dlAverageThroughput'][:-3])
            pair = (src_ip_int, seID)
            if pair not in unique_pairs:
                unique_pairs.add(pair)
            data.append({
                "seID":int(seID),
                "SrcIp":src_ip_int,
                "DstIp":dst_ip_int,
                "SrcPort":int(SrcPort),
                "DstPort":int(DstPort),
                "ulPeakThroughput": ulPeakThroughput, #-  lastUlVolume,
                "dlPeakThroughput": dlPeakThroughput, #- lastDlVolume,
                "ulAveragePacketThroughput": ulAveragePacketThroughput, #- lastTotalVolume,
                "dlAveragePacketThroughput": dlAveragePacketThroughput, #- lastUlPacket,
                "ulPeakPacketThroughput": ulPeakPacketThroughput, #- lastDlPacket,
                "dlPeakPacketThroughput": dlPeakPacketThroughput,
                "ulAverageThroughput": ulAverageThroughput, #- lastDlPacket,
                "dlAverageThroughput": dlAverageThroughput,
                 'timestamp':timestamp #- lastTotalPacket
            })
        df = pd.DataFrame(data)
    #     logging.info(f"[DEBUG] the created data frame is {df}")
    return df, unique_pairs


def get_traffic_prediction(features):
    """ Send real-time data to MLflow Model Server and get prediction """
    data = {"dataframe_split": features.to_dict(orient="split")}
#     logging.info(f"the data is {data}")
#     logging.info(f"info: the current_inference_link{config.current_inference_link}")
    if not config.current_inference_link:
        logging.info("Warning: ML inference link is not set yet. Cannot send data.")
        return None


    try:
        response = requests.post(config.current_inference_link, json=data)
        if response.status_code == 200:
            response_dict = response.json()
            predictions = response_dict['predictions']
            logging.info(f"the response from the mlflow is: {predictions}")
            return predictions
        else:
            logging.info(f"MLflow request failed: {response.status_code}")
            return None
    except Exception as e:
        logging.info(f"Error calling MLflow Model: {e}")
        return None

