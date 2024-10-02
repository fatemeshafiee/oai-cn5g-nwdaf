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

logging.basicConfig(level=logging.INFO)
api = Blueprint('api', __name__)

@api.route('/abnormal_behaviour/suspicion_of_ddos_attack', methods=['GET'])
def handle_suspicion_of_ddos_attack():
    df = create_dataframe()
    ue_list = []
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        logging.info(f"the row data is: {row_dict}")
        scaler.learn_one(row_dict)
        scaled_data = scaler.transform_one(row_dict)
        score = model.score_one(scaled_data)
        is_anomaly = model.classify(score)
        if is_anomaly:
            ue_list.append(row_dict)
            logging.info(row_dict)
    ddos_report = []
    if len(ue_list) != 0:
        for ue_info in ue_list:
            ddos_report.append({
                "ue_ip":".".join(str(ipaddress.ip_address(ue_info['SrcIp'])).split(".")[::-1]),
                "target_ip":".".join(str(ipaddress.ip_address(ue_info['DstIp'])).split(".")[::-1]),
#                 "pdu_sess_id":pdu_seid,
                "seid":ue_info['seID'],
            }
            )
    response_data = {'ddos_entries': ddos_report}
    return_data = jsonify(response_data)
    logging.info(return_data)

    return jsonify(response_data)





