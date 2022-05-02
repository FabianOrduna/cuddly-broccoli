import generate_features 
import helper_etl
import pandas as pd
import numpy as np


def generateFeatures(global_yaml):
    
    current_year = date.today().year 
    season_year = current_year
    if (date.today().month < 8):
        season_year = current_year-1
    

    conn = helper_etl.database_connection(global_yaml)

    table_season = helper_etl.get_schema('match_fof', conn)

    clean_data = generate_features.readDataFromSeason(table_season,conn,season_year,True)
    last_data = generate_features.FeatureEngineer(season_year, clean_data)

    match_to_predict = generate_features.readDataFromSeason(table_season, conn, season_year, False)

    match_to_predict = pd.DataFrame(match_to_predict)
    match_to_predict.columns = ['id','season','date','local','away','local_goals','away_goals']
    aux = match_to_predict[(match_to_predict['local_goals'].isna())]
    aux = aux.sort_values(by="date")

    data_final = []
    none_teams = {}
    for match in aux.itertuples():
        if match[4] not in none_teams and match[5] not in none_teams:
            data_final.append(match)
        if(match[4] not in none_teams):
            none_teams[match[4]] = 1
        if(match[5] not in none_teams):
            none_teams[match[5]] = 1

    future_matches_df = pd.DataFrame(data_final).drop(columns = 'Index')
    played_matches_df = pd.DataFrame(clean_data)
    played_matches_df.columns = ['id', 'season', 'date', 'local', 'away', 'local_goals', 'away_goals']

    aux_df = pd.concat([played_matches_df, future_matches_df], ignore_index=True, sort=False)

    aux = aux_df.values.tolist()

    match_to_predict = generate_features.FeatureEngineer(2021, aux)
    match_to_predict_df = pd.DataFrame(match_to_predict)

    match_to_predict_df.columns = ["season","local","local_goles","local_goles_recibidos","local_dif_goles", "local_jornadas_jugadas", "visita","visita_goles","visita_goles_recibidos","visita_dif_goles", "visita_jornadas_jugadas", "ganador"] 

    match_to_predict_df = match_to_predict_df[match_to_predict_df['ganador']=="nose"].drop(columns = 'ganador')
    match_to_predict_df = match_to_predict_df.astype({"local_goles": int,"local_goles_recibidos": int, "local_dif_goles": int, "visita_goles": int, "visita_goles_recibidos": int, "visita_dif_goles": int})

    predictions_schema = helper_etl.get_schema('predictions', conn)
    helper_etl.get_schema('predictions', conn)
    helper_etl.insert_data(conn, predictions_schema, match_to_predict_df.to_dict('records'))