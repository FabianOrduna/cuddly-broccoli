"""MLOPs and predictions DAG"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago
import os
from GenerateFeatures import generateFeatures
from GeneratePredictions import generatePrediction
from endpoint import generatePredictionEndpoint

path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(path, 'dag_mlops.py')
yaml_path = os.path.join(path, 'yaml.yml')
model_path = os.path.join(path, "model.pkl")

params = {
    'script': script_path,
    'global_yaml': yaml_path,
    'model_path': model_path
}

dag = DAG(
    dag_id='cuddly_broccoli_dag_mlops',
    schedule_interval='0 3 * * *',
    start_date=days_ago(2),
    tags=['bash', 'python', 'mlops'],
    max_active_runs=3
)

#bash_task = BashOperator(
#    dag=dag,
#    params=params,
#    task_id='bash_task',
#    bash_command='python3 {{ params.script}} --global_yml yaml.yml'
#)

fetch_task = PythonOperator(
    dag=dag,
    task_id = 'fetch',
    provide_context=True,
    python_callable=generateFeatures,
    op_kwargs={'global_yaml': params['global_yaml']}
)

predict_task = PythonOperator(
    dag=dag,
    task_id = 'predict',
    provide_context=True,
    python_callable=generatePrediction,
    op_kwargs={'global_yaml': params['global_yaml'],
              'model_path' :params['model_path']}
)

endpoint_task = PythonOperator(
    dag=dag,
    task_id = 'endpoint',
    provide_context=True,
    python_callable=generatePredictionEndpoint,
    op_kwargs={'global_yaml': params['global_yaml']}
)

fetch_task >> predict_task
fetch_task >> endpoint_task

