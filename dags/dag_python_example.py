from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Definir los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 8),  # Ajusta la fecha de inicio según sea necesario
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Función Python que se ejecutará en el DAG
def mi_funcion():
    now = datetime.now()
    print(f"Fecha de ejecución: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("¡Hola! Este es un DAG de prueba ejecutando Python.")

# Definir el DAG
dag = DAG(
    'dag_python_example',
    default_args=default_args,
    description='Ejemplo de DAG ejecutando Python dentro de Airflow',
    schedule_interval='30 1 * * *',  # Ejecutar todos los días a la 1:30 AM UTC
    catchup=False,
)

# Definir la tarea que ejecuta la función Python
run_python_task = PythonOperator(
    task_id='run_python_function',
    python_callable=mi_funcion,
    dag=dag,
)

# Estructura del DAG
run_python_task

