# ETL Process

We decided to do an ETL process in order to have our databases in a normalized way ready to directly input to the machine learning model. The ETL script can be found in this folder by the name of **api.ipynb**.

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

- Extraction

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

- Transform
    - Shape
        - [Schema on write](https://www.techopedia.com/definition/30899/schema-on-write)
            - Reduce/Add columns
            - Data types
        - Columnar to row based
    - Data quality
    - PII/Masking
    - [Normalization](https://docs.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
    - MLOPs
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
