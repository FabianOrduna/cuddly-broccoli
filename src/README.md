# ETL Process

We decided to go through an ETL process in order to have our database ready for direct input into machine learning models in a standardized way. The ETL script can be found in this folder by the name of **api.ipynb**.

### Step by step:

Our ETL process was done using a Vertex AI instance named "api-football". These instances have the advantage that they are already configured Notebooks with JupyterLab3 and the common data science libraries preinstalled. 

### Libraries: 

* yaml
* requests
* pandas
* json
* sqlalchemy
* pg8000
* pymysql

### Extraction

Passwords and connection parameters are loaded as environment variables using a yaml file.

```
with open('footballYaml.yaml') as f:
  config = yaml.load(f, Loader=yaml.FullLoader)
football_key = config['football_key']
user = config["db_user"]
db_pass = config["db_pass"]
db_name = config["db_name"]
db_host = config["db_host"]
```

The requests were build based on the [Python sample extraction scripts](https://www.api-football.com//documentation-v3#section/Sample-Scripts/Python) of API we used. This request needs to specify the URL of the API, a querystring which is sort of a filter, headers where we specify our API key, and the GET method. In the end this information is downloaded in a JSON format.

This procedure was repeated for season games and player information.


### Transform

Our transformation starts by transforming our request JSONs to lists of dictionaries. 

The season data was organized by season year, match date, match id, local team name, local team id, away team name, away team id, local goals and away goals. 

The players statistics data was organized by page, season, player_id, player_name, age, height, weight, injured, team_id, appearences, minutes, position, rating, shots, goals, assists, passes_accuracy, total_duels and won_duels. In order to get the information we considered that:

- This endpoint returns the players for whom the profile and statistics data are available. Note that it is possible that a player has statistics for 2 teams in the same season in case of transfers. In that case the key is team_id and player_id.
 
- The statistics are calculated according to the team id, league id and season.

- The players id are unique in the API.

- This endpoint uses a pagination system, you can navigate between the different pages thanks to the page parameter.

- The season 2019 has 33 pages, season 2020 has 37 pages and season 2021 has 39 pages.

- One request per page, each of one has 20 different player's statistics.

### Load

We used Google Cloud SQL to store our database, the name of our instance is "cuddly-broccoli-instance". To stablish the connection to SQL service we used the sqlalchemy library and the following engine url create code: 

```
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
        username=db_user,  
        password=db_pass,  
        host=db_hostname,  
        port=db_port,  
        database=db_name  
    )
)
```

The structure requeries to pass the user, password, host ip, port and database name (*cuddly-broccoli-db*). 

Once the connection was stablished and the database created, we had to create two tables and load the previously requested data.

We created the tables *match* and **COMPLETAR** with the Table() function. *match* tiene las columnas id, season, match_date, local_team, away_team, local_goals and away_goals. Then, data was loaded with the insert_data(function). 

These tables are visible using the select() command in python. 

match table preview:

| id | season | match_date | local_team | away_team | local_goals | away_goals |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2019 | datetime.date(2019, 8, 9) | 'Liverpool' | 'Norwich' | 4 | 1 |
| 2 | 2019 | datetime.date(2019, 8, 10) | 'West Ham' | 'Manchester City' | 0 | 5 |
| 3 | 2019 | datetime.date(2019, 8, 10) | 'Bournemouth' | 'Sheffield Utd' | 1 | 1 |
| 4 | 2019 | datetime.date(2019, 8, 10) | 'Burnley' | 'Southampton' | 3 | 0 |
| 5 | 2019 | datetime.date(2019, 8, 10) | 'Crystal Palace' | 'Everton' | 0 | 0 |
| 6 | 2019 | datetime.date(2019, 8, 11) | 'Leicester' | 'Wolves' | 0 | 0 |
| 7 | 2019 | datetime.date(2019, 8, 10) | 'Watford' | 'Brighton' | 0 | 3 |
| 8 | 2019 | datetime.date(2019, 8, 10) | 'Tottenham' | 'Aston Villa' | 3 | 1 |
| 9 | 2019 | datetime.date(2019, 8, 11) | 'Newcastle' | 'Arsenal' | 0 | 1 |
| 10 | 2019 | datetime.date(2019, 8, 11) | 'Manchester United' | 'Chelsea' | 4 | 0 |
| ... | ... | ... | ... | ... | ... | ... |

### References
- [SQL connect.](https://cloud.google.com/sdk/gcloud/reference/sql/connect)
- [Delete in SQL.](https://docs.sqlalchemy.org/en/14/core/tutorial.html#deletes)
- [Connect App Engine.](https://cloud.google.com/sql/docs/postgres/connect-app-engine-standard#private-ip_1)
