from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 8),
}

with DAG('dag_simple', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    start = DummyOperator(task_id='inicio')
    end = DummyOperator(task_id='fin')

    start >> end  # Dependencia entre tareas
