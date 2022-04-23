import yaml
import requests
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Boolean, create_engine, Float, and_
from sqlalchemy.sql import select, insert, delete
from datetime import date

#global_yaml = 'yaml.yml'

def season_data(year,global_yaml):
    with open(global_yaml) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    football_key = config['football_key']
    url = "https://v3.football.api-sports.io/fixtures"
    querystring = {"league":"39","season":year}
    payload={}
    headers = {
        'x-rapidapi-key': football_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.request("GET", url, headers=headers, params=querystring,  data=payload).json()
    season_data = []
    for row in response["response"]:
        season_data.append({"season":row["league"]["season"],
                               "match_date":row["fixture"]["date"],
                               "match_id":row["fixture"]["id"],
                               "local_team":row["teams"]["home"]["name"],
                                "local_team_id":row["teams"]["home"]["id"],
                               "away_team":row["teams"]["away"]["name"],
                                "away_team_id":row["teams"]["away"]["id"],
                               "local_goals":row["goals"]["home"],
                               "away_goals":row["goals"]["away"]})
    return season_data

def player_stats(year, page,global_yaml):
    with open(global_yaml) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    football_key = config['football_key']
    url = "https://v3.football.api-sports.io/players"
    querystring = {"league":"39","season":year, "page":page}
    
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': football_key
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    statistic_data = []
    for row in response["response"]:
        statistic_data.append({"page":response['paging']["current"],
                               "season":row["statistics"][0]["league"]["season"],
                               "player_id":row["player"]["id"],
                               "player_name":row["player"]["name"],
                               "age":row["player"]["age"],
                               "height":row["player"]["height"],
                               "weight":row["player"]["weight"],
                               "injured":row["player"]["injured"],
                               "team_id":row["statistics"][0]["team"]["id"],
                               "appearences":row["statistics"][0]["games"]["appearences"],
                               "minutes":row["statistics"][0]["games"]["minutes"],
                               "position":row["statistics"][0]["games"]["position"],
                               "rating":row["statistics"][0]["games"]["rating"],
                               "shots":row["statistics"][0]["shots"]["total"],
                               "goals":row["statistics"][0]["goals"]["total"],
                               "assists":row["statistics"][0]["goals"]["assists"],
                               "passes_accuracy":row["statistics"][0]["passes"]["accuracy"],
                               "total_duels":row["statistics"][0]["duels"]["total"],
                               "won_duels":row["statistics"][0]["duels"]["won"]
                              })
        
    return statistic_data

def database_connection(global_yaml):
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

    conn = sqlalchemy.create_engine(
    # Equivalent URL:
    # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name  # e.g. "my-database-name"
        )
    )
    conn.connect()
    return conn 

def get_schema(table_name, conn):
    metadata = MetaData(bind=None)
    return Table(table_name, metadata, autoload=True, autoload_with=conn)

def readMatchesFromSeason(table_name, conn, season, clean):
    # If clean == True, it does not return the matches with NA goals 
    if (table_name != "match_fof"):
        return None
    table = get_schema(table_name, conn)
    if clean == True:
        stmt = select(table.columns).where(and_(table.columns.season == season, table.columns.local_goals != None))
    else:
        stmt = select(table.columns).where(and_(table.columns.season == season))
    connectionDB = conn.connect()
    return connectionDB.execute(stmt).fetchall()

def readStatsFromSeason(table, conn, season, clean):
    # If clean == True, it does not return the matches with NA goals 
    if (table_name != "statistics_f1"):
        return None
    table = get_schema(table_name, conn)
    if clean == True:
        stmt = select(table.columns).where(and_(table.columns.season == season, table.columns.appearences != None))
    else:
        stmt = select(table.columns).where(and_(table.columns.season == season))
    connectionDB = conn.connect()
    return connectionDB.execute(stmt).fetchall()

def insert_data(conn, table, data):
    ins = table.insert()
    conn.execute(ins, data)

def insert_matches(conn, table_name, data):
    if (table_name != "match_fof"):
        return None
    table = get_schema(table_name, conn)
    insert_data(conn, table, data) 

def insert_statistics(conn, table_name, data):
    if (table_name != "statistics_f1"):
        return None
    table = get_schema(table_name, conn)
    insert_data(conn, table, data) 
    
def clear_match_season(year, conn):
    table = get_schema("match_fof", conn)
    stmt = delete(table).where(table.c.season == year)
    conn.execute(stmt)
    return print("Season", year, "has been deleted :)")

def main_delete(global_yaml):
    # Connecting to the database
    conn = database_connection(global_yaml)
    
    # Table and season year
    matches_table_name = "match_fof"
    current_year = date.today().year 
    season_year = current_year
    if (date.today().month < 8):
        season_year = current_year-1
    
    # Update match results for current season
    clear_match_season(season_year, conn)
    
def main_insert(global_yaml):
    # Connecting to the database
    conn = database_connection(global_yaml)
    
    # Table and season year
    matches_table_name = "match_fof"
    current_year = date.today().year 
    season_year = current_year
    if (date.today().month < 8):
        season_year = current_year-1
    
    matches_current_year = season_data(season_year,global_yaml)
    insert_matches(conn, matches_table_name , matches_current_year)
    print("This week's data has been updated successfully!")
