import os
import json
import requests
import google.generativeai as genai
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Configurar API Key de Gemini
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY", "tu_api_key")
genai.configure(api_key=GENAI_API_KEY)

# Configuración de la API de Airflow
AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
AIRFLOW_AUTH = ("admin", "admin")

# 🔹 Función para obtener el estado de los DAGs en Airflow
# 🔹 Función para obtener el estado de los DAGs en Airflow
def get_airflow_dags():
    try:
        response = requests.get(f"{AIRFLOW_URL}/dags", auth=AIRFLOW_AUTH, timeout=10)
        if response.status_code == 200:
            dags = response.json().get("dags", [])
            
            # Filtrar solo los DAGs activos y no pausados
            active_dags = [
                {"id": dag["dag_id"], "estado": "activo"} 
                for dag in dags if dag["is_active"] and not dag["is_paused"]
            ]
            
            return json.dumps(active_dags) if active_dags else "No hay DAGs activos actualmente."
        else:
            return f"Error al consultar Airflow: {response.status_code}"
    except requests.RequestException as e:
        return f"Error de conexión con Airflow: {str(e)}"
    except Exception as e:
        return f"Error al obtener DAGs de Airflow: {str(e)}"


# 🔹 Función para hacer una consulta a Gemini
def query_gemini(question: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)
        return response.text if response else "Error en la generación de respuesta con Gemini"
    except Exception as e:
        return f"Error en Gemini: {str(e)}"

# 🔹 Función principal del agente AI
def airflow_ai_agent(**kwargs):
    ti = kwargs["ti"]  # Obtener contexto de ejecución

    # Obtener la pregunta desde el conf del DAGRun
    dag_run = kwargs.get("dag_run")
    question = dag_run.conf.get("question", "¿Cuáles son los DAGs activos en Airflow?") if dag_run else "¿Cuáles son los DAGs activos en Airflow?"

    # Obtener lista de DAGs
    dags_info = get_airflow_dags()

    # Generar el prompt para Gemini
    prompt = f"{question}\nLista de DAGs disponibles en Airflow: {dags_info}"

    # Hacer la consulta a Gemini
    response = query_gemini(prompt)

    # Guardar respuesta en XCom
    ti.xcom_push(key="ai_response", value=response)

    return response

# 🔹 Definir el DAG de Airflow
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "ai_airflow_agent",
    default_args=default_args,
    schedule_interval=None,  # Solo se ejecuta manualmente
    catchup=False,
    tags=["ai", "gemini", "airflow"]
) as dag:

    run_ai_agent = PythonOperator(
        task_id="run_ai_agent",
        python_callable=airflow_ai_agent,
        provide_context=True  # Importante para recibir kwargs
    )

    run_ai_agent
