"""Retrains and uploads the model for MLOps"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago
import os
import helper_train
from helper_train import retrain

path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(path, 'dag_retrain.py')
yaml_path = os.path.join(path, 'yaml.yml')

params = {
    'script': script_path,
    'global_yaml': yaml_path
}

dag = DAG(
    dag_id='cuddly_broccoli_dag_retrain',
    schedule_interval='0 0 15 * *',
    start_date=days_ago(2),
    tags=['bash', 'python', 'mlops'],
    max_active_runs=3
)

retrain_task = PythonOperator(
    dag=dag,
    task_id = 'retrain',
    provide_context=True,
    python_callable=retrain,
    op_kwargs={'global_yaml': params['global_yaml']}
)

