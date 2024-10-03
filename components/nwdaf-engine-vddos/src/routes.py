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
    ddos_report = []
    ddos_info = {}
    for index, row in df.iterrows():
        y = model.predict(row[['ulVolume','dlVolume','totalVolume','ulPacket','dlPacket','totalPacket']])
        if y == 1:
            ddos_info.add(df[['SrcIp','DstIp','SrcPort','DstPort']][index])
    if len(ddos_info) != 0:
        for ue_info in ddos_info:
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





