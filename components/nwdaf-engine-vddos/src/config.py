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
# * Author: Fatemeh Shafiei Ardestani
# * Description: nwdaf-engine-vddos configuration parameters.
# */

import os
from pymongo import MongoClient
import pickle
import joblib
import pickle

# Load the model from the file





# Env Variables
SERVER_PORT = os.environ.get('SERVER_PORT','8989')
MONGODB_URI = os.environ.get('MONGODB_URI','mongodb://localhost:27017')
NWDAF_DATABASE_NAME = os.environ.get('MONGODB_DATABASE_NAME', 'testing')
MONGODB_COLLECTION_NAME_UPF = os.environ.get('MONGODB_COLLECTION_NAME_UPF', 'upf')

# Global variables
client = MongoClient(MONGODB_URI)
nwdaf_db = client[NWDAF_DATABASE_NAME]
upf_collection = nwdaf_db[MONGODB_COLLECTION_NAME_UPF]
current_time = None
# Model parameters
#components/nwdaf-engine-vddos/models/random_forest_model_pickle.pkl
with open('models/random_forest_model_pickle.pkl', 'rb') as file:
    model = pickle.load(file)