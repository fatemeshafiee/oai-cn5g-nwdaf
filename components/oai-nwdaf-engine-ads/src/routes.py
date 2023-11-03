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

api = Blueprint('api', __name__)  
logging.basicConfig(level=logging.INFO)

@api.route('/abnormal_behaviour/unexpected_large_rate_flow', methods=['GET'])
def handle_unexpected_large_rate_flow_request():
    df = create_dataframe()
    logging.info(df[['timestamp', 'value_total']])
    # Get the usefull rows of the DataFrame.
    df_seq = df[['hour', 'value_ul']].tail(seq_dim)
    seq = ulrf_scaler.transform(df_seq)
    # Add model to calculate anomaly probability for sequence.
    seq = np.reshape(seq, (1, seq_dim, num_features))
    predict_seq = ulrf_model.predict(seq)
    mae = np.mean(np.abs(predict_seq[:,:,1:] - seq[:,:,1:]), axis=1)
    distance = np.abs(mae - distance_threshold)
    anomaly_prob = np.minimum(distance / max_distance_threshold, 1)
    logging.info("unexpected_large_rate_flow probability is: %s", anomaly_prob[0][0])
    ratio = int(anomaly_prob * 100)
    response_data = {'ratio': ratio}
    # send anomaly probability to client.
    return jsonify(response_data)