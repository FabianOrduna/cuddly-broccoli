import sys
import subprocess
# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
#'pg8000<=1.16.5'])
import yaml
import requests
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Boolean, create_engine, Float, and_
from sqlalchemy.sql import select, insert, delete, update
from datetime import date
from helper_etl import database_connection, season_data, get_schema, readMatchesFromSeason, insert_data


#Table predictions

def generate_prediction_table(conn):
    meta = MetaData()
    match = Table(
        'predictions', meta, 
        Column('id', Integer, primary_key = True),
        Column('season', Integer),
        Column('local', String),
        Column('local_goles', Integer),
        Column('local_goles_recibidos', Integer),
        Column('local_dif_goles', Integer),
        Column('local_jornadas_jugadas', Integer),
        Column('visita', String),
        Column('visita_goles', Integer),
        Column('visita_goles_recibidos', Integer),
        Column('visita_dif_goles', Integer),
        Column('visita_jornadas_jugadas', Integer),
        Column('prediction_result', String),
        Column('real_result', String)
    )
    meta.create_all(conn)

#Correr feature engineering
def readDataFromSeason(table, connection, season, clean):
    if clean == True:
        stmt = select(table.columns).where(and_(table.columns.season == season, table.columns.local_goals != None))
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
                elif(partido[5]!=partido[6]):
                    resPredictor = 'nose'
            
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


#def readPredictions(connection, clean):
#    table = get_schema('predictions', conn)
#    if clean == True:
#        stmt = select(table.columns).where(and_(table.columns.prediction_result == None)
#    else:
#        stmt = select(table)
#    return conn.execute(stmt).fetchall()
                                           
def readPredictions(conn, not_predicted):
    table = get_schema('predictions', conn)
    if (not_predicted == True):
        stmt = select(table.columns).where(and_(table.columns.prediction_result == None))
    else:
        stmt = select(table)
    return conn.execute(stmt).fetchall()

def update_prediction(conn, season, local, away, result):
    table = get_schema('predictions', conn)
    stmt = (update(table).where(and_(table.c.season==season,table.c.local == local, table.c.visita == away)).values({"prediction_result":result}))
    return conn.execute(stmt)
    