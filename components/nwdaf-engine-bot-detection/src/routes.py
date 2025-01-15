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
#TODO
@api.route('/abnormal_behaviour/suspicion_of_ddos_attack', methods=['GET'])
def handle_ue_profile():
    df, unique_pairs = create_dataframe()
    summary_per_ip = create_ue_profile(df)
    g_feature = create_graph_feature(df)
#     df.to_csv('df.csv', index=False)
#     summary_per_ip.to_csv('summary_per_ip.csv', index=False)
#     if len(ddos_info) != 0:
#         for ue_info in ddos_info:
#             ddos_report.append({
#                 "ue_ip":".".join(str(ipaddress.ip_address(ue_info[1])).split(".")),
#                 "target_ip":".".join(str(ipaddress.ip_address(ue_info[2])).split(".")),
# #                 "pdu_sess_id":pdu_seid,
#                 "seid":ue_info[0]
# #                  "prob": 1
#             }
#             )
#     response_data = {'ddos_entries': ddos_report}
    global current_time
    logging.info(f"the df is: {df}")
    bot_report = []
    bot_info = set()
    predictions = rf_model.predict(g_feature)
    indices = [i for i, pred in enumerate(predictions) if pred == 1]
    for index in indices:
        bot_ip =  g_features.iloc[index]['src_ip']
        for pair in unique_pairs:
            if pair[0] == bot_ip:
                bot_report.append({
                "ue_ip":".".join(str(ipaddress.ip_address(ip)).split(".")),
                "target_ip": "*.*.*.*",
                "seid":pair[1]
                })
    response_data = {'ddos_entries': bot_report}
    return_data = jsonify(response_data)
    logging.info(return_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    logging.info(f"the report for this event created: {current_time}")

    return jsonify(response_data)





