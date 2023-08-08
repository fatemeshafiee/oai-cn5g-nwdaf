from flask import Flask, request, jsonify
from pymongo import MongoClient
from tensorflow import keras
import numpy as np
import pickle 
import pymongo
import pandas as pd
import os
import logging

# --------------------------------------------------- CONFIG -------------------------------------------------------
app = Flask(__name__)

# read MongoDB connection information from environment variables
mongo_uri = os.environ.get('MONGODB_URI')
nwdaf_db_name = os.environ.get('MONGODB_DATABASE_NAME', 'testing')
amf_collection_name = os.environ.get('MONGODB_COLLECTION_NAME_AMF', 'amf')
smf_collection_name = os.environ.get('MONGODB_COLLECTION_NAME_SMF', 'smf')

# connect to MongoDB database
client = MongoClient(mongo_uri)
nwdaf_db = client[nwdaf_db_name]
amf_collection = nwdaf_db[amf_collection_name]
smf_collection = nwdaf_db[smf_collection_name]

# Load ML Models and scalers
ulrf_model = keras.models.load_model('models/unexpected_large_rate_flow/model.h5')
ulrf_scaler = pickle.load(open('models/unexpected_large_rate_flow/scaler.pkl', 'rb'))

# Some ML-based anomaly detection parameters - related to model
seq_dim = 12
num_features = 2
distance_threshold = 0.26
max_distance_threshold = 2

# --------------------------------------------------- ROUTES -------------------------------------------------------
@app.route('/abnormal_behaviour/unexpected_large_rate_flow', methods=['GET'])
def handle_unexpected_large_rate_flow_request():
    
    df = create_dataframe()

    print (df[['timestamp', 'value_total']])
    # Get the usefull rows of the DataFrame.
    df_seq = df[['hour', 'value_ul']].tail(seq_dim)

    seq = ulrf_scaler.transform(df_seq)

    #print (seq)
    # Convert the last_n DataFrame to a numpy array.
    #seq = df_seq.to_numpy()

    # Add model to calculate anomaly probability for sequence.
    seq = np.reshape(seq, (1, seq_dim, num_features))
    predict_seq = ulrf_model.predict(seq)
    mae = np.mean(np.abs(predict_seq[:,:,1:] - seq[:,:,1:]), axis=1)
    distance = np.abs(mae - distance_threshold)
    anomaly_prob = np.minimum(distance / max_distance_threshold, 1)

    print("")
    print("unexpected_large_rate_flow probability is: "+str(anomaly_prob[0][0]))
    print("")

    # Convert probability to percentage
    ratio = int(anomaly_prob * 100)
    response_data = {'ratio': ratio}

    # send anomaly probability to client.
    return jsonify(response_data)

# --------------------------------------------------- FUNCTIONS -------------------------------------------------------

def add_time_columns(df, timestamp_col):
    df['timestamp'] = pd.to_datetime(df[timestamp_col], unit='s')
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    return df

def create_dataframe():
    data = []
    for doc in smf_collection.find():
        for qosmon in doc['qosmonlist']:
            data.append({
                "timestamp": qosmon['timestamp'],
                "pduseid": qosmon['pduseid'],
                "value_ul": qosmon['customized_data']['usagereport']['volume']['uplink'] ,
                "value_dl": qosmon['customized_data']['usagereport']['volume']['downlink'],
                "value_total": qosmon['customized_data']['usagereport']['volume']['total']
            })
    # Create a pandas dataframe
    df = pd.DataFrame(data)
    df = add_time_columns(df, 'timestamp')
    return df

# --------------------------------------------------- MAIN -------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8080,debug=True)