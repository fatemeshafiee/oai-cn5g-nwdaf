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
# * Description: This file contains oai-nwdaf-engine-ads server routes.
# */

from src.config import *
from src.functions import *
from flask import Blueprint, jsonify
import logging
from datetime import datetime
import pandas as pd
from datetime import datetime
logging.basicConfig(level=logging.INFO)
api = Blueprint('api', __name__)
counter = 0
@api.route('/abnormal_behaviour/suspicion_of_ddos_attack', methods=['GET'])
def handle_ue_profile():
    counter += 1
    df, unique_pairs = create_dataframe()
    if counter == update_time:
        summary_per_ip = create_ue_profile(df)
        dict_data = summary_per_ip.to_dict(orient='records')
        for rec in dict_data:
            ip = rec['SrcIp']
            key = 'SrcIp'
            query = {key : ip}
            update = {"$set": rec}
            ue_profile_collection.update_one(query, update, upsert=True)
    g_feature = create_graph_feature(df)
    G = build_graph_per_batch(g_feature)
    G_features = extract_grapgh_features(G, ['10.42.0.2', '10.42.0.3', '10.42.0.4', '10.42.0.5', '10.42.0.6', '10.42.0.7'])

    global current_time
#     logging.info(f"the df is: {df}")
    bot_report = []
    bot_info = set()
    predictions = rf_model.predict(G_features[['in_degree', 'out_degree', 'w_in_degree', 'w_out_degree', 'betweenness', 'LCC']])
    indices = [i for i, pred in enumerate(predictions) if pred == 1]
    for index in indices:
        bot_ip =  G_features.iloc[index]['host_ip']
        for pair in unique_pairs:
            if pair[0] == bot_ip:
                bot_report.append({
                "ue_ip":".".join(str(ipaddress.ip_address(int(bot_ip))).split(".")),
                "target_ip": "*.*.*.*",
                "seid":pair[1]
                })
    response_data = {'ddos_entries': bot_report}
    return_data = jsonify(response_data)
    logging.info(return_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    logging.info(f"the report for this event created: {current_time}")

    return jsonify(response_data)





