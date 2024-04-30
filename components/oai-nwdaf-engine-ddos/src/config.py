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
# * Description: oai-nwdaf-engine-ads configuration parameters.
# */

import os
from pymongo import MongoClient
import pickle
from tensorflow import keras

# Env Variables
SERVER_PORT = os.environ.get('SERVER_PORT','8989')
MONGODB_URI = os.environ.get('MONGODB_URI','mongodb://localhost:27017')
NWDAF_DATABASE_NAME = os.environ.get('MONGODB_DATABASE_NAME', 'testing')
MONGODB_COLLECTION_NAME_AMF = os.environ.get('MONGODB_COLLECTION_NAME_AMF', 'amf')
MONGODB_COLLECTION_NAME_SMF = os.environ.get('MONGODB_COLLECTION_NAME_SMF', 'smf')

# Global variables
client = MongoClient(MONGODB_URI)
nwdaf_db = client[NWDAF_DATABASE_NAME]
amf_collection = nwdaf_db[MONGODB_COLLECTION_NAME_AMF]
smf_collection = nwdaf_db[MONGODB_COLLECTION_NAME_SMF]

# Autoencoder parameters
ulrf_model = keras.models.load_model('models/unexpected_large_rate_flow/model.h5')
ulrf_scaler = pickle.load(open('models/unexpected_large_rate_flow/scaler.pkl', 'rb'))
seq_dim = 12
num_features = 2
distance_threshold = 0.26
max_distance_threshold = 2