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

The players data was organized by local team id, local team players id, away team id, away team players id and ratings.

### Load

- Load
    - Error handling
    - Sinks
        - Database
        - Data lake
        - Web server / application

- [ ]  Include a README in your `src` folder explaining:
    - [ ]  Whether you are performing an ELT or ETL job
    - [ ]  Which GCP resources you are using (**Google Cloud SQL, Compute Engine, Vertex AI, etc)** and the names of each instance
    - [ ]  A brief summary of the transformations you are performing
