"""
DAG: Pipeline de Análise de Vendas - Distribuidora Kwanza Comercial (Angola)

Fluxo:
1. Gera (ou verifica) os dados sintéticos
2. Carrega os CSVs para o schema 'raw' no PostgreSQL
3. Executa dbt run (staging → intermediate → marts)
4. Executa dbt test
"""

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Configurações
DATA_DIR = Path("/opt/airflow/data/raw")
DBT_DIR = Path("/opt/airflow/dbt")
SCRIPTS_DIR = Path("/opt/airflow/scripts")

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def carregar_csv_para_raw(**context):
    """Carrega os três CSVs para o schema raw no PostgreSQL."""
    import pandas as pd
    from sqlalchemy import create_engine, text

    hook = PostgresHook(postgres_conn_id="postgres_dw")
    engine = hook.get_sqlalchemy_engine()

    ficheiros = {
        "clientes": DATA_DIR / "clientes.csv",
        "produtos": DATA_DIR / "produtos.csv",
        "vendas": DATA_DIR / "vendas.csv",
    }

    with engine.begin() as conn:
        # Garante que o schema existe
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

        for tabela, caminho in ficheiros.items():
            if not caminho.exists():
                raise FileNotFoundError(f"Ficheiro não encontrado: {caminho}")

            df = pd.read_csv(caminho)
            print(f"A carregar {tabela}: {len(df)} linhas...")

            # Escreve na tabela raw.<tabela> (substitui se já existir)
            df.to_sql(
                name=tabela,
                con=conn,
                schema="raw",
                if_exists="replace",
                index=False,
                method="multi",
                chunksize=500,
            )
            print(f"✓ {tabela} carregado com sucesso")

    print("Carga para o schema RAW concluída.")


with DAG(
    dag_id="pipeline_vendas_angola",
    default_args=default_args,
    description="Pipeline batch de análise de vendas - contexto angolano",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["vendas", "angola", "dbt", "batch", "fundacao"],
) as dag:

    # 1. Gera os dados (caso ainda não existam)
    gerar_dados = BashOperator(
        task_id="gerar_dados_sinteticos",
        bash_command=f"""
            if [ ! -f {DATA_DIR}/vendas.csv ]; then
                echo "A gerar dados sintéticos..."
                python {SCRIPTS_DIR}/gerar_dados.py
            else
                echo "Dados já existem. A saltar geração."
            fi
        """,
    )

    # 2. Carrega CSVs → PostgreSQL (schema raw)
    carregar_raw = PythonOperator(
        task_id="carregar_raw",
        python_callable=carregar_csv_para_raw,
    )

    # 3. dbt run
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
            cd {DBT_DIR} && \
            dbt run --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}
        """,
    )

    # 4. dbt test
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
            cd {DBT_DIR} && \
            dbt test --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}
        """,
    )

    # 5. Documentação (opcional, gera docs)
    dbt_docs = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=f"""
            cd {DBT_DIR} && \
            dbt docs generate --profiles-dir {DBT_DIR} --project-dir {DBT_DIR} || true
        """,
    )

    # Ordem de execução
    gerar_dados >> carregar_raw >> dbt_run >> dbt_test >> dbt_docs
