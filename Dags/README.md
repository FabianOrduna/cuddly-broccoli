# Airflow

The instance is named "Airflow4". The IP access is generated when the instance is started. The process has two steps: delete and insert, the last one depends on the first execution and is indicated on the dag.py file as **insert>>delete**. The description of the process is as follow:

* ### Delete:
In this step the airflow instance execute the function _main_delete_ that consist in delete the information into the _match_fof_ table. This table contains the results of the last matches. 

* ### Insert:
After the table was delete in the first process the instance will execute a second step that consist in insert new information into the _match_fof_ table. First, the process aks to the API the information with the last results of the week and second, the process insert the new information on the _match_fof_ table. 

Finally, the data is available on GCP table in postgresql. The idea is that the airflow excecute the process every week on wednesday.
