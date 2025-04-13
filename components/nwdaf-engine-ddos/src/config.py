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
#  Author: Fatemeh Shafiei Ardestani
#  Created on: 2025-04-06
#*/

import os
from pymongo import MongoClient
import pickle
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional
from tensorflow.keras.regularizers import l2
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


# Define your model architecture
DDoS_Detection_model = Sequential()
DDoS_Detection_model.add(Bidirectional(LSTM(64, activation='tanh', kernel_regularizer=l2(0.01), return_sequences=False), input_shape=(5, 11)))
DDoS_Detection_model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
DDoS_Detection_model.add(Dense(1, activation='sigmoid', kernel_regularizer=l2(0.01)))

# Load the weights from the saved model file
DDoS_Detection_model.load_weights("models/ddos/brnn_model.h5")

# Compile the model
DDoS_Detection_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# TO Check with our own model
# seq_dim = 12
# num_features = 2
# distance_threshold = 0.26
# max_distance_threshold = 2