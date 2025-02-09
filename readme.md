# 🚀 Airflow + PostgreSQL + TimescaleDB + Redis en Docker

Este proyecto proporciona un entorno completo para ejecutar **Apache Airflow** con **PostgreSQL, TimescaleDB y Redis** utilizando `docker-compose`.

## 📁 Estructura del Proyecto

```bash
/opt/proyecto
├── dags/        # Almacena los DAGs de Airflow
├── logs/        # Logs generados por Airflow
├── scripts/     # Scripts auxiliares
├── plugins/     # Plugins adicionales para Airflow
└── docker-compose.yml
```

Ejecuta el siguiente script para configurar las rutas necesarias:

```sh
# Crear directorios
mkdir -p /opt/proyecto/dags
mkdir -p /opt/proyecto/logs
mkdir -p /opt/proyecto/scripts
mkdir -p /opt/proyecto/plugins
```

## ⚙️ Servicios Incluidos

| Servicio           | Descripción                                        |
|--------------------|----------------------------------------------------|
| **postgres**      | Base de datos principal para Airflow (PostgreSQL 16) |
| **timescaledb**   | Base de datos TimescaleDB para almacenamiento optimizado |
| **redis**         | Cola de mensajes para Airflow                        |
| **airflow-webserver** | Interfaz web de Apache Airflow                   |
| **airflow-scheduler** | Scheduler de Airflow para ejecutar DAGs          |
| **airflow-init**  | Inicialización de la base de datos de Airflow        |

## 🔧 Configuración

Antes de ejecutar los contenedores, se deben definir algunas variables de entorno para asegurar que Airflow y los servicios asociados funcionen correctamente. Ejecuta los siguientes comandos en la terminal:

```sh
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)
export _AIRFLOW_WWW_USER_USERNAME=admin
export _AIRFLOW_WWW_USER_PASSWORD=admin
export GOOGLE_API_KEY="tu_api_key_aquí"
```

> **Nota:** Se recomienda guardar estas variables en un archivo `.env` y añadirlo a `.gitignore` para evitar exponer credenciales.

## 🚀 Cómo Ejecutar el Entorno

### 🔄 Arrancar Airflow 🚀
Para iniciar el entorno de Airflow, ejecuta:

```sh
docker compose up -d
```

Este comando levantará todos los servicios necesarios y los dejará en ejecución en segundo plano.

### 🛠 Reiniciar Desde Cero

Si necesitas limpiar todos los volúmenes y reconstruir los contenedores:

```sh
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)
export _AIRFLOW_WWW_USER_USERNAME=admin
export _AIRFLOW_WWW_USER_PASSWORD=admin
export GOOGLE_API_KEY="tu_api_key_aquí"

docker compose down -v

docker compose up --build
```

Esto eliminará los datos persistentes y reconstruirá los contenedores.

### 🌍 Acceder a Airflow
Después de ejecutar `docker compose up`, puedes acceder a la interfaz web de Airflow en:

🔗 **[http://localhost:8080](http://localhost:8080)**

| Usuario  | Contraseña |
|----------|-----------|
| `admin`  | `admin`   |

### 🛑 Detener el Entorno
Para detener los contenedores sin eliminar los volúmenes de datos:

```sh
docker compose down
```

Si también quieres eliminar los volúmenes de datos:

```sh
docker compose down -v
```

## 📌 Servicios y Puertos

| Servicio          | Puerto | Descripción                                 |
|------------------|--------|---------------------------------------------|
| **PostgreSQL**   | 5432   | Base de datos de Airflow                    |
| **TimescaleDB**  | 5433   | Base de datos para series temporales        |
| **Redis**        | 6379   | Cola de mensajes de Airflow                  |
| **Airflow Web UI** | 8080  | Interfaz gráfica de Airflow                 |

## 🤖 Pruebas del Agente de Airflow con Google Gemini

### 1️⃣ **Ejecutar el DAG de prueba**
Puedes ejecutar manualmente el DAG `ai_airflow_agent` enviando una pregunta a Gemini mediante la API de Airflow:

```sh
curl -X POST "http://localhost:8080/api/v1/dags/ai_airflow_agent/dagRuns" \
  --user "admin:admin" \
  -H "Content-Type: application/json" \
  -d '{
    "conf": {
      "question": "¿Cuáles son los DAGs en estado activo?"
    }
  }'
```

### 2️⃣ **Consultar la respuesta en XCom**
Para ver la respuesta de Gemini, revisa los valores almacenados en XCom:

```sh
curl -X GET "http://localhost:8080/api/v1/dags/ai_airflow_agent/dagRuns/latest/taskInstances/run_ai_agent/xcomEntries" \
  --user "admin:admin" | jq
```

Si todo está correctamente configurado, deberías ver una respuesta como esta:

```json
{
  "xcom_entries": [
    {
      "key": "ai_response",
      "value": "Los DAGs activos actualmente son: [dag_1, dag_2, dag_3]"
    }
  ]
}
```

### 3️⃣ **Depuración en caso de error**
Si el DAG no se ejecuta correctamente:

- **Revisa los logs de ejecución** en la interfaz web de Airflow.
- **Verifica que la variable `GOOGLE_API_KEY` esté correctamente configurada** en `.env`.
- **Asegúrate de que el DAG está activo** y habilitado en la UI de Airflow.

---

Este README te proporciona todo lo necesario para levantar y probar un entorno de Airflow completo con integración de PostgreSQL, TimescaleDB, Redis y un agente de IA basado en Google Gemini. 🚀

