import helper_etl
from datetime import date

# Connecting to the database
conn = helper_etl.database_connection()

# Table and season year
matches_table_name = "match_fof"
current_year = date.today().year 
season_year = current_year
if (date.today().month < 8):
    season_year = current_year-1

# Update match results for current season
helper_etl.clear_match_season(season_year, conn)

match_tmp = helper_etl.readMatchesFromSeason(matches_table_name, conn, season_year, False)

if (len(match_tmp) == 0): 
    matches_current_year = helper_etl.season_data(season_year)
    helper_etl.insert_matches(conn, matches_table_name , matches_current_year)
    print("This week's data has been updated successfully!")
else: 
    print("An error has ocurred :(") 