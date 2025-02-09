🚀 Airflow + PostgreSQL + TimescaleDB + Redis en Docker

Este proyecto proporciona un entorno completo para ejecutar Apache Airflow con PostgreSQL, TimescaleDB y Redis utilizando docker-compose.

📁 Estructura del Proyecto

/opt/proyecto
├── dags/        # Almacena los DAGs de Airflow
├── logs/        # Logs generados por Airflow
├── scripts/     # Scripts auxiliares
├── plugins/     # Plugins adicionales para Airflow
└── docker-compose.yml

⚙️ Servicios Incluidos

Servicio

Descripción

postgres

Base de datos principal para Airflow (PostgreSQL 16)

timescaledb

Base de datos TimescaleDB para almacenamiento optimizado

redis

Cola de mensajes para Airflow

airflow-webserver

Interfaz web de Apache Airflow

airflow-scheduler

Scheduler de Airflow para ejecutar DAGs

airflow-init

Inicialización de la base de datos de Airflow

🔧 Configuración

Antes de ejecutar los contenedores, se deben definir algunas variables de entorno para asegurar que Airflow funcione correctamente. Ejecuta los siguientes comandos en la terminal:

export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)
export _AIRFLOW_WWW_USER_USERNAME=admin
export _AIRFLOW_WWW_USER_PASSWORD=admin

🚀 Cómo Ejecutar el Entorno

🔄 Arrancar Airflow 🚀

Para iniciar el entorno de Airflow, ejecuta:

docker compose up

Este comando levantará todos los servicios necesarios y los dejará en ejecución.

🛠 Reiniciar Desde Cero

Si necesitas limpiar todos los volúmenes y reconstruir los contenedores:

export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)
export _AIRFLOW_WWW_USER_USERNAME=admin
export _AIRFLOW_WWW_USER_PASSWORD=admin

docker compose down -v

docker compose up --build

Esto eliminará los datos persistentes y reconstruirá los contenedores.

🌍 Acceder a Airflow

Después de ejecutar docker compose up, puedes acceder a la interfaz web de Airflow en:

🔗 http://localhost:8080

Usuario: adminContraseña: admin

🛑 Detener el Entorno

Para detener los contenedores sin eliminar los volúmenes de datos:

docker compose down

Si también quieres eliminar los volúmenes de datos:

docker compose down -v

📌 Notas Adicionales

Asegúrate de que Docker y docker-compose estén correctamente instalados en tu máquina.

postgres y timescaledb están expuestos en los puertos 5432 y 5433, respectivamente.

Los DAGs deben guardarse en la carpeta dags/ dentro del directorio del proyecto.

Si tienes problemas con permisos, revisa la configuración de volúmenes y usa chmod para dar permisos de escritura en /opt/proyecto/.

