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

from flask import Blueprint, jsonify
from src.config import *
from src.functions import *
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler
api = Blueprint('api', __name__)  
logging.basicConfig(level=logging.INFO)

@api.route('/abnormal_behaviour/ddos', methods=['GET'])
def handle_ddos_detection_request():
    df = create_dataframe()
    logging.info(df[["Dst IP", "Dst Port", "Src IP", "Src Port", "Protocol", "pduseid"]])
    # Get the usefull rows of the DataFrame.
    X = df.iloc[:, :-1]
    scalar = StandardScaler(copy=True, with_mean=True, with_std=True)
    scalar.fit(X)
    X = scalar.transform(X)

    features = len(X[0])
    samples = X.shape[0]
    logging.info(X.shape)

    train_len = 5 #would it make any problem? When we have less packets?
    input_len = samples - train_len
    I = np.zeros((samples - train_len, train_len, features))

    for i in range(input_len):
        temp = np.zeros((train_len, features))
        for j in range(i, i + train_len - 1):
            temp[j-i] = X[j]
        I[i] = temp
    predict = DDoS_Detection_model.predict(I)

    predictn = predict.flatten().round()
    df = df[train_len:len(X)]
#     suspicious_Flows = df[predictn == 0]
    predictn = predictn.tolist()


    suspicious_ues = df["Src IP"].tolist()
    suspicious_pdu_seid = df["pduseid"].tolist()
    ratios = predict.flatten().tolist()

    for ue_ip, pdu_seid, ratio in zip(suspicious_ues, suspicious_pdu_seid, ratios):
        if not np.isnan(ratio) and ration > 0.5:
            ddos_entries.append({
                "ue_ip":ue_ip,
                "pdu_sess_id":pdu_seid,
                "ratio": ratio
            })
    

    response_data = {'ddos_entries': ddos_entries}
    # send anomaly probability to client.
    return_data = jsonify(response_data)
    logging.info(return_data)

    return jsonify(response_data)