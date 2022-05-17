# endpoint DAG

import generate_features
import helper_etl
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.svm import SVC
import subprocess
import sys
import json
import yaml

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

#global_yaml = '../../footballYaml.yml'
def generatePredictionEndpoint(global_yaml):
    
    with open(global_yaml) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        
    ENDPOINT_ID = config["ENDPOINT_ID"]
    PROJECT_ID = config["PROJECT_ID"]
    INPUT_DATA_FILE = config["INPUT_DATA_FILE"]
    REGION = config["REGION"]


    conn = helper_etl.database_connection(global_yaml)



    match_to_predict_df = generate_features.readPredictions(conn, False)
    match_to_predict_df = pd.DataFrame(match_to_predict_df)
    print(match_to_predict_df)
    match_to_predict_df.columns = ["index", "season","local","local_goles","local_goles_recibidos","loca_dif_goles", "local_jornadas_jugadas", "visita","visita_goles","visita_goles_recibidos","visita_dif_goles", "visita_jornadas_jugadas", "prediction_result", "real_result"] 
    match_to_predict_df= match_to_predict_df.drop(columns = ["index","local",'season', 'prediction_result', 'real_result', 'visita',])
    match_to_predict_df["local_jornadas_jugadas"] = match_to_predict_df["local_jornadas_jugadas"].apply(str)
    match_to_predict_df["visita_jornadas_jugadas"] = match_to_predict_df["visita_jornadas_jugadas"].apply(str)


    #matches = {'instances':[]}
    lista = []
    for i in range(0,len(match_to_predict_df)):
        match_to_predict = match_to_predict_df.loc[i].to_dict()
        #model = pd.read_pickle("model.pkl")
    #model = pd.read_pickle(model_path)
        lista.append(match_to_predict)
    # writing a json with the input values for the model

    #print(lista)
    matches = {'instances':lista}
    print(matches)
    with open("default-pred.json", "w") as outfile:
        json.dump(matches, outfile,cls=NpEncoder)


    # predicting

    #!curl \
    #-X POST \
    #-H "Authorization: Bearer $(gcloud auth print-access-token)" \
    #-H "Content-Type: application/json" \
    #https://us-central1-prediction-aiplatform.googleapis.com/v1alpha1/projects/$PROJECT_ID/locations/$REGION/endpoints/$ENDPOINT_ID:predict \
    #-d "@default-pred.json" > "results.json"



    bashCmd = 'curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" https://us-central1-prediction-aiplatform.googleapis.com/v1alpha1/projects/'+str(PROJECT_ID)+'/locations/'+str(REGION)+'/endpoints/'+str(ENDPOINT_ID)+':predict -d "@default-pred.json" > "results.json"'
    subprocess.run(bashCmd, shell = True, stdout=subprocess.PIPE)
