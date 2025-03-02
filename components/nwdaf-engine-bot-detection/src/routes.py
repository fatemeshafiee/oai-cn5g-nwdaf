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
# */

from src.config import *
import src.config as config
from src.functions import *
from flask import Blueprint, jsonify, Flask, request
import logging
import pandas as pd
import requests
from datetime import datetime, timedelta
from uuid import uuid4
import logging
import threading
from src.schemes import *

logging.basicConfig(level=logging.INFO)
api = Blueprint('api', __name__)
def extract_ml_model_url(notification: dict) -> Optional[str]:
    event_notifs = notification.get("mLEventNotifs")
    if not event_notifs:
        return None

    for notif in event_notifs:
        ml_addr = notif.get("mLFileAddr") or notif.get("mLModelAdrf")
        if ml_addr and isinstance(ml_addr, dict):
            ml_url = ml_addr.get("mLModelUrl") or ml_addr.get("mlFileFqdn")
            if ml_url:
                return ml_url
    return None

def     subscribe_to_ml_model_prov(ml_model_prov_url: str, notif_uri: str):

    subscription = NwdafMLModelProvSubsc(
        mLEventSubscs=[
            MLEventSubscription(
                mLEvent=NwdafEvent(nwdafEvent="ABNORMAL_BEHAVIOUR"),
                mLEventFilter={}
            )
        ],
        notifUri=notif_uri,
        notifCorreId=str(uuid4()),
        eventReq=ReportingInformation(
            immRep=True,
            repPeriod=10
        )
    )

    headers = {"Content-Type": "application/json"}
    logging.info(f"Sending Subscription Request to {ml_model_prov_url}/subscribe")
    logging.info(f"Request Payload: {subscription.model_dump()}")
    try:
        response = requests.post(
            f"{ml_model_prov_url}/subscribe",
            json=subscription.model_dump(mode="json"),
            headers=headers
        )
        response.raise_for_status()
        logging.info(f"Subscription Successful: {response.json()}")
        resp_json = response.json()
        logging.info(f"Subscription Successful: {resp_json}")
        ml_url = extract_ml_model_url(resp_json)
        if ml_url:

            config.current_inference_link = ml_url
            logging.info(f"Updated current_inference_link: {config.current_inference_link}")
        else:
            logging.info("No ML model URL found in the notification response.")
        return resp_json
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in Subscription: {e}")
        return None
@api.route("/notifications", methods=["POST"])
def receive_notification():

    global current_inference_link

    try:
        data = request.json
        if not data:
            logging.error("Received empty notification")
            return jsonify({"error": "Empty request"}), 400
        if isinstance(data, str):  # ADDED: Check if data is a string
            data = json.loads(data)  # ADDED: Convert it to a dict

        logging.info(f"Received Notification: {data}")
        notification = NwdafMLModelProvNotif(**data)

        for event in notification.eventNotifs:
            if event.mLFileAddr and event.mLFileAddr.mLModelUrl:
                current_inference_link = event.mLFileAddr.mLModelUrl  # Added: Update the inference link
                logging.info(f"Updated ML Inference Link: {current_inference_link}")

        return jsonify({"status": "Updated inference link"}), 200

    except Exception as e:
        logging.error(f"Invalid notification received: {e}")
        return jsonify({"error": "Invalid notification"}), 400

@api.route('/abnormal_behaviour/suspicion_of_ddos_attack', methods=['GET'])
def handle_ue_profile():
    global counter
    global update_time
    counter += 1
    df, unique_pairs = create_dataframe()
    df.to_csv('df.csv', index=False)
    if counter == update_time:
        summary_per_ip = create_ue_profile(df)
        dict_data = summary_per_ip.to_dict(orient='records')
        for rec in dict_data:
            ip = rec['SrcIp']
            key = 'SrcIp'
            query = {key : ip}
            update = {"$set": rec}
            ue_profile_collection.update_one(query, update, upsert=True)
        counter = 0
    g_feature = create_graph_feature(df)
    G = build_graph_per_batch(g_feature)
    G_features = extract_grapgh_features(G, ['10.42.0.2', '10.42.0.3', '10.42.0.4', '10.42.0.5', '10.42.0.6', '10.42.0.7'])

    global current_time
#     logging.info(f"the df is: {df}")
    bot_report = []
    bot_info = set()
    predictions = get_traffic_prediction(G_features[['in_degree', 'out_degree', 'w_in_degree', 'w_out_degree', 'betweenness', 'LCC']])
#     rf_model.predict(G_features[['in_degree', 'out_degree', 'w_in_degree', 'w_out_degree', 'betweenness', 'LCC']])
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



