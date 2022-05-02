# Airflow

The instance is named "Airflow4". It is scheduled to run mondays and sundays. 

## ETL

The process has two steps: delete and insert, insert depends on the succesfull execution of delete and is indicated on the dag.py file as **insert>>delete**. The description of the process is as follow:


* ### Delete:
In this step the airflow instance execute the function _main_delete_ that consist in delete the information into the _match_fof_ table. This table contains the results of the last matches. 

* ### Insert:
After the table was delete in the first process the instance will execute a second step that consist in insert new information into the _match_fof_ table. First, the process aks to the API the information with the last results of the week and second, the process insert the new information on the _match_fof_ table. 

Finally, the data is available on GCP table in postgresql. The idea is that the airflow excecute the process every week on wednesday.

## MLOPS

First we need to gather the data to predict next week's matches. Then, we predict and store the results in a postgres table.

* ### Fetch:
The airflow instance runs the function _fun1_ to fetch the data that we will use to predict. It saves the data in the table _predictions_.

* ### Predict
We feed the model with the data from _predictions_ and save the scored in the _prediction\_result_ table.
