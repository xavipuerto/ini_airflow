FROM apache/airflow:2.10.4

USER root

RUN pip install --no-cache-dir \
    pydantic-ai \
    google-generativeai \
    httpx \
    requests \
    pandas

USER airflow
