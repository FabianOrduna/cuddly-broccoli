import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pg8000<=1.16.5'])
import pg8000
from sqlalchemy import MetaData, create_engine
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import time
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Boolean, Float, and_
from sqlalchemy.sql import select, insert
import pandas as pd
import yaml
import requests
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
from google.cloud import storage
import os 

# Pipeline, Gridsearch, train_test_split
from sklearn.model_selection import train_test_split, GridSearchCV

# Plot the confusion matrix at the end of the tutorial
from sklearn.metrics import plot_confusion_matrix

# Classification Models
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier

# Functions

def create_bucket(bucket_name):
    """Taken from: https://www.thecodebuzz.com/create-google-cloud-gcp-storage-bucket-python/"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    storage
    try:
    #bucket.storage_class = "Standard Storage"
        new_bucket = storage_client.create_bucket(bucket, location="us-central1")
 
        print("Created bucket successfully {} in location {}".format(new_bucket.name, new_bucket.location))
    except: 
        print("Bucket already exists")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Taken from: https://www.thecodebuzz.com/python-upload-files-download-files-google-cloud-storage/ """
    """Uploads a file to the google storage bucket."""
    #storage_client = storage.Client()
    storage_client = storage.Client.from_service_account_json(json_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to Storage Bucket with Bob name {} successfully .".format(source_file_name, destination_blob_name)) 
    
def readDataFromSeason(table, connection, season, clean):
    if clean == True:
        stmt = select(table.columns).where(and_(table.columns.season == season, table.columns.local_goals != None))
    else:
        stmt = select(table.columns).where(and_(table.columns.season == season))
    connectionDB = connection.connect()
    return connectionDB.execute(stmt).fetchall()

def readStatsFromSeason(table, connection, season, clean):
    if clean == True:
        stmt = select(table.columns).where(and_(table.columns.season == season, table.columns.appearences != None))
    else:
        stmt = select(table.columns).where(and_(table.columns.season == season))
    connectionDB = connection.connect()
    return connectionDB.execute(stmt).fetchall()

def sumaGoles(golesEquipo, totalPartidos):
    favor = 0
    contra = 0
    diferencia = 0
    for i in range(totalPartidos):
        #print("sumando el partido "+str(i))
        favor+=golesEquipo[i][0]
        contra+=golesEquipo[i][1]
        diferencia+=golesEquipo[i][2]
    return [favor, contra, diferencia]

def FeatureEngineer(anio,partialRes):
    equipos = {} # para contar los partidos jugados por equipo
    totalGoals = {} # primero a favor, luego en contra, luego diferencia
    for res in partialRes:
        if(res[1]==anio and res[5] != None): # != None validdation required for non played matches
            #datos de equipos
            local = res[3]
            visita = res[4]

            #datos de goles
            goles_local = res[5]
            goles_visita = res[6]

            if(not (local in equipos)):
                equipos[local] = 0

            if(not (visita in equipos)):
                equipos[visita] = 0

            #logica para guardar los goles por equipo y el acumulado
            if(local in totalGoals):
                totalGoals[local].append([goles_local,goles_visita, goles_local-goles_visita])
            else:
                totalGoals[local] = [[goles_local,goles_visita, goles_local-goles_visita]]

            if(visita in totalGoals):
                totalGoals[visita].append([goles_visita, goles_local, goles_visita-goles_local])
            else:
                totalGoals[visita] = [[goles_visita, goles_local, goles_visita-goles_local]]


    featureEng = []

    for partido in partialRes:
        if (partido[1]==anio and partido[5] != None): # != None validdation required for non played matches
            #print(partido)
            local = partido[3]
            visita = partido[4]
            goles_acumulados_local = sumaGoles(totalGoals[local], equipos[local])
            goles_acumulados_visita = sumaGoles(totalGoals[visita], equipos[visita])
            
            #ahora se define si gana el local, el visita o empate
            resPredictor = 'empate'
            if(partido[5]>partido[6]):
                resPredictor = 'local'
            else:
                if(partido[5]<partido[6]):
                    resPredictor = 'visita'
            
            featureEng.append([partido[1],
                        local,
                        goles_acumulados_local[0],
                        goles_acumulados_local[1],
                        goles_acumulados_local[2],
                        equipos[local],#partidos jugados hasta el momento              
                        visita,
                        goles_acumulados_visita[0],
                        goles_acumulados_visita[1],
                        goles_acumulados_visita[2],
                        equipos[visita],#partidos jugados hasta el momento  
                        resPredictor]
                             )
            equipos[local] = equipos[local]+1
            equipos[visita] = equipos[visita]+1


    return featureEng

def ajustaPipeline(grid_param_in, X_train_in,y_train_in):
    #transformador de columnas
    
    col_transformer = ColumnTransformer(
                    transformers=[
                        ('onehot', OneHotEncoder(handle_unknown = 'ignore'), ["local","visita"] )],
                    remainder='drop',
                    n_jobs=-1
                    )   
    
    pipe = Pipeline([('encoder', col_transformer), ("classifier", RandomForestClassifier())])
    # se crea gridsearch sobre pipeline
    gridsearch = GridSearchCV(pipe, param_grid=grid_param_in, cv=5, verbose=0,n_jobs=-1, scoring='accuracy') # Fit grid search

    start_time = time.time()
    best_model = gridsearch.fit(X_train_in,y_train_in)
    total_time = time.time() - start_time
    return best_model, total_time

def printmodelresult(mensaje, modelo,tiempo, X_t, y_t):
    print("====================================")
    print(mensaje)
    print("====================================")
    accuracy = modelo.score(X_t, y_t)
    print("tiempo estimado [segundos]")
    print(tiempo)
    print("Accuracy")
    print(accuracy)
    # creating a confusion matrix
    #plot_confusion_matrix(modelo, X_t, y_t)
    y_predict = modelo.predict(X_t)
    print(classification_report(y_t, y_predict))
    return accuracy

def retrain(global_yaml): 
    with open(global_yaml) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    db_user = config["db_user"]
    db_pass = config["db_pass"]
    db_name = config["db_name"]
    db_host = config["db_host"]
    host_args = db_host.split(":")
    if len(host_args) == 1:
        db_hostname = db_host
        db_port = 5432
    elif len(host_args) == 2:
        db_hostname, db_port = host_args[0], int(host_args[1])
    
    conn = sqlalchemy.create_engine("postgresql+pg8000://"+db_user+":"+db_pass+"@"+db_host+"/"+db_name)
    conn.connect()

    metadata = MetaData(bind=None)
    table = Table(
        'match_fof', 
        metadata, 
        autoload=True, 
        autoload_with=conn
    )

    metadata = MetaData(bind=None)
    table_stats = Table(
        'statistics_f1', 
        metadata, 
        autoload=True, 
        autoload_with=conn
    )

    todos_features = None

    seasons_TRAIN = [2018,2019]

    for year in seasons_TRAIN:
        fe_year = FeatureEngineer(year,readDataFromSeason(table,conn,year,True))
        if(todos_features == None):
            todos_features = fe_year
        else:
            todos_features = todos_features + fe_year

    test_features = None

    season_TEST = [2020,2021]

    for year in season_TEST:
        fe_year = FeatureEngineer(year,readDataFromSeason(table,conn,year,True))
        if(test_features == None):
            test_features = fe_year
        else:
            test_features = test_features + fe_year

    columnas = ["temporada","local","local_goles","local_goles_recibidos","locaL_dif_goles", "local_jornadas_jugadas", "visita","visita_goles","visita_goles_recibidos","visita_dif_goles", "visita_jornadas_jugadas", "ganador"]

    datos_fe = pd.DataFrame(todos_features)
    datos_fe.columns = columnas
    X_train = datos_fe.iloc[: , 1:-1]
    y_train = datos_fe.iloc[: , -1]

    datos_test = pd.DataFrame(test_features)
    datos_test.columns = columnas
    X_test = datos_test.iloc[: , 1:-1]
    y_test = datos_test.iloc[: , -1]


    grid_param_lr = [{"classifier": [LogisticRegression()],
                   "classifier__penalty": ['l2'],
                   "classifier__C": np.logspace(0, 4, 10),
                   "classifier__solver":['newton-cg','saga','sag','liblinear'], ##This solvers don't allow L1 penalty
                   "classifier__max_iter":[20000]
                    }
                 ] 


    


    regresion_model, tiempo_regresion = ajustaPipeline(grid_param_lr, X_train,y_train)


    


    accuracy_regresion = printmodelresult("Modelo de regresion logistica",regresion_model,tiempo_regresion,X_test, y_test)




    accuracy_max = accuracy_regresion
    winner_model = regresion_model

    


    grid_param_knn = [{"classifier": [KNeighborsClassifier()],
                     "classifier__n_neighbors": [1,3,5,7,10,15,20,25,50,100],
                     "classifier__weights":['uniform','distance'],
                     "classifier__algorithm":['auto','ball_tree','kd_tree']
                  }]




    knn_model, tiempo_knn = ajustaPipeline(grid_param_knn, X_train,y_train)




    accuracy_knn = printmodelresult("Modelo de Knn",knn_model,tiempo_knn,X_test, y_test)




    if accuracy_max < accuracy_knn:
        accuracy_max = accuracy_knn
        winner_model = knn_model

    


    grid_param_svm = [{"classifier": [SVC(kernel='linear', probability=True, random_state=0)],
                     "classifier__C": [0.00001,0.0001,0.001,0.01,0.1,1,10],
                     "classifier__kernel":['linear', 'rbf']}]




    svm_model, tiempo_svm = ajustaPipeline(grid_param_svm, X_train,y_train)




    accuracy_svm = printmodelresult("Modelo de SVM",svm_model,tiempo_svm,X_test, y_test)




    if accuracy_max < accuracy_svm:
        accuracy_max = accuracy_svm
        winner_model = svm_model




    grid_param_rfc = [{"classifier": [RandomForestClassifier()],
                     "classifier__n_estimators": [10, 100, 1000],
                     "classifier__max_depth":[5,8,15,25,30,None],
                     "classifier__min_samples_leaf":[1,2,5,10,15,100],
                     "classifier__max_leaf_nodes": [2, 5,10]}]




    random_forest_model, tiempo_random_forest = ajustaPipeline(grid_param_rfc,X_train,y_train)




    accuracy_randomf = printmodelresult("Modelo de Random Forest",random_forest_model,tiempo_random_forest,X_test, y_test)




    if accuracy_max < accuracy_randomf:
        accuracy_max = accuracy_randomf
        winner_model = random_forest_model



    grid_param_gbc = [{"classifier": [GradientBoostingClassifier(subsample=0.5)],
                     "classifier__n_estimators": [50,100,150],
                     "classifier__learning_rate":[0.001,0.01,0.05,0.1,0.5,1,2,3],
                     "classifier__max_depth":[3,5,10]
                  }]




    gbc_model, tiempo_gbc = ajustaPipeline(grid_param_gbc,X_train,y_train)




    accuracy_xgboost = printmodelresult("Modelo de Gradient Boosting",gbc_model,tiempo_gbc,X_test, y_test)




    if accuracy_max < accuracy_xgboost:
        accuracy_max = accuracy_xgboost
        winner_model = gbc_model



    grid_param_perc = [{"classifier": [MLPClassifier()],
                     "classifier__max_iter": [150,200,300,450],
                     "classifier__learning_rate":['constant', 'invscaling', 'adaptive'],
                     "classifier__solver":['lbfgs', 'sgd', 'adam']
                  }]



    perc_model, tiempo_perc = ajustaPipeline(grid_param_perc,X_train,y_train)




    accuracy_perceptron = printmodelresult("Modelo de Perceptron",perc_model,tiempo_perc,X_test, y_test)




    if accuracy_max < accuracy_perceptron:
        accuracy_max = accuracy_perceptron
        winner_model = perc_model

    


    print("El mejor modelo de acuerdo con los entrenamientos fue: ")
    print(winner_model)
    print("Con un accuracy de: " + str(accuracy_max)) 




    with open('winner_model.pkl', 'wb') as handle:
        pickle.dump(winner_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    new_bucket = "cuddly-broccoli"

    upload_blob(new_bucket,"winner_model.pkl","dags/model.pkl")
    
    # Delete pkl from vm

    os.remove("./winner_model.pkl")
