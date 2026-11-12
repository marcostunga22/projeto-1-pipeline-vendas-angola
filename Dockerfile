FROM apache/airflow:2.9.3-python3.11

USER root

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Instala dbt e outras dependências Python
RUN pip install --no-cache-dir \
    dbt-core==1.8.7 \
    dbt-postgres==1.8.2 \
    pandas \
    psycopg2-binary \
    openpyxl \
    apache-airflow-providers-postgres \
    sqlalchemy


# Garante que o dbt está no PATH
ENV PATH="/home/airflow/.local/bin:${PATH}"
