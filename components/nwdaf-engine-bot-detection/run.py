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
# * Description: This is the main file of oai-nwdaf-engine-ads.
# */

from flask import Flask
from src.config import SERVER_PORT
from src.routes import api, subscribe_to_ml_model_prov
import threading

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/')

def start_subscription():

    ml_model_prov_url = "http://modelprov-svc.open5gs.svc.cluster.local:8000"

    notif_uri = "http://nwdaf-engine-bot-detection.open5gs.svc.cluster.local:8080/notifications"
    subscribe_to_ml_model_prov(ml_model_prov_url, notif_uri)

if __name__ == '__main__':
    subscription_thread = threading.Thread(target=start_subscription)
    subscription_thread.start()
    app.run(host='0.0.0.0', threaded=True, port=SERVER_PORT,debug=True)