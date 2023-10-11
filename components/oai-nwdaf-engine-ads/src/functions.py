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

def add_time_columns(df, timestamp_col):
    df['timestamp'] = pd.to_datetime(df[timestamp_col], unit='s')
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    return df

def create_dataframe():
    data = []
    for doc in smf_collection.find():
        for qosmon in doc['qosmonlist']:
            data.append({
                "timestamp": qosmon['timestamp'],
                "pduseid": qosmon['pduseid'],
                "value_ul": qosmon['customized_data']['usagereport']['volume']['uplink'] ,
                "value_dl": qosmon['customized_data']['usagereport']['volume']['downlink'],
                "value_total": qosmon['customized_data']['usagereport']['volume']['total']
            })
    # Create a pandas dataframe
    df = pd.DataFrame(data)
    df = add_time_columns(df, 'timestamp')
    return df