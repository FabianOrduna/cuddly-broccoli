"""Demo DAG for using Bash and Python Operators"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago
import os
from helper_etl import main_delete
from helper_etl import main_insert

path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(path, 'etl_delete.py')
params = {
    'script': script_path,
    'global_yaml': 'yaml.yml'
}

dag = DAG(
    dag_id='cuddly_broccoli_dag',
    schedule_interval='0 0 * * 1,7',
    start_date=days_ago(2),
    tags=['bash', 'python', 'lab8', 'demo'],
    max_active_runs=1
)

#bash_task = BashOperator(
#    dag=dag,
#    params=params,
#    task_id='bash_task',
#    bash_command='python3 {{ params.script}} --global_yml yaml.yml'
#)

delete_task = PythonOperator(
    dag=dag,
    task_id = 'delete',
    provide_context=True,
    python_callable=main_delete,
    op_kwargs={'global_yaml': params['global_yaml']}
)

insert_task = PythonOperator(
    dag=dag,
    task_id = 'insert',
    provide_context=True,
    python_callable=main_insert,
    op_kwargs={'global_yaml': params['global_yaml']}
)

delete_task >> insert_task


