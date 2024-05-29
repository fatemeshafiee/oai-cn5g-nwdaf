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
import ipaddress


from sklearn.preprocessing import StandardScaler
api = Blueprint('api', __name__)  
logging.basicConfig(level=logging.INFO)

@api.route('/abnormal_behaviour/ddos', methods=['GET'])
def handle_ddos_detection_request():
    df = create_dataframe()
    ddos_entries = []
    logging.info(df[["Dst IP", "Dst Port", "Src IP", "Src Port", "Protocol", "pduseid", "seid"]])
    # Get the usefull rows of the DataFrame.
    # These are the features we care about
    # ['Flow Duration', 'Fwd Packet Length Std', 'ACK Flag Count', 'Protocol', 'Total Fwd Packet', 'Total Bwd packets',
    # 'Total Length of Fwd Packet', 'Total Length of Bwd Packet']
    X = df.iloc[:, :-2]
    for ip in X ["Src IP"].unique():
        X_PER_UE  = X[X["Src IP"]==ip]
        df_per_ue = df[df["Src IP"]==ip]
        scalar = StandardScaler(copy=True, with_mean=True, with_std=True)
        scalar.fit(X_PER_UE)
        X_PER_UE = scalar.transform(X_PER_UE)

        features = len(X_PER_UE[0])
        samples = X_PER_UE.shape[0]
        logging.info(X_PER_UE.shape)

        train_len = 5 #would it make any problem? When we have less packets?
        input_len = samples - train_len
        I = np.zeros((samples - train_len, train_len, features))

        for i in range(input_len):
            temp = np.zeros((train_len, features))
            for j in range(i, i + train_len - 1):
                temp[j-i] = X_PER_UE[j]
            I[i] = temp
        predict = DDoS_Detection_model.predict(I)

        predictn = predict.flatten().round()
        
        df_per_ue = df_per_ue[train_len:len(X_PER_UE)]
#     suspicious_Flows = df[predictn == 0]
        predictn = predictn.tolist()


        suspicious_ues = df_per_ue["Src IP"].tolist()
        targets = df_per_ue["Dst IP"].tolist()
        suspicious_pdu_seid = df_per_ue["pduseid"].tolist()
        suspicious_seid = df_per_ue["seid"].tolist()
        ratios = predict.flatten().tolist()
    
        for ue_ip, target, pdu_seid, seid, ratio in zip(suspicious_ues, targets, suspicious_pdu_seid, suspicious_seid, ratios):
            if not np.isnan(ratio) and ratio > 0.5:
                ddos_entries.append({
                "ue_ip":".".join(str(ipaddress.ip_address(ue_ip)).split(".")[::-1]),
                "target_ip":".".join(str(ipaddress.ip_address(target)).split(".")[::-1]),
                "pdu_sess_id":pdu_seid,
                "seid":seid,
                "ratio": ratio

                })
    

    response_data = {'ddos_entries': ddos_entries}
    # send anomaly probability to client.
    return_data = jsonify(response_data)
    logging.info(return_data)

    return jsonify(response_data)