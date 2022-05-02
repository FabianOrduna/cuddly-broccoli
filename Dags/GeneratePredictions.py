import generate_features 
import helper_etl
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.svm import SVC

def generatePrediction(global_yaml,model_path):
    conn = helper_etl.database_connection(global_yaml)

    match_to_predict_df = generate_features.readPredictions(conn, True)
    match_to_predict_df = pd.DataFrame(match_to_predict_df)
    match_to_predict_df.columns = ["index", "season","local","local_goles","local_goles_recibidos","local_dif_goles", "local_jornadas_jugadas", "visita","visita_goles","visita_goles_recibidos","visita_dif_goles", "visita_jornadas_jugadas", "prediction_result", "real_result"] 

    #model = pd.read_pickle("model.pkl")
    model = pd.read_pickle(model_path)
    result = model.predict(match_to_predict_df.drop(columns = ['season', 'prediction_result', 'real_result']))

    match_to_predict_df['prediction_result'] = result

    for match in match_to_predict_df.itertuples():
        generate_features.update_prediction(conn, match[2], match[3], match[8], match[13])