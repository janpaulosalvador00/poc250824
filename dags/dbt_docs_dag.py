from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import timedelta

# Definições dos parâmetros padrão e configuração do DAG
default_args = {
    'owner': 'dbt-docs-1550',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(dag_id='dbt_docs_dag',
         schedule_interval='@daily',
         start_date=datetime(2024, 9, 6),
         catchup=False) as dag:

    # Tarefa para servir a documentação do DBT
    serve_docs_task = BashOperator(
        task_id='serve_docs_task',
        bash_command='dbt docs serve --port 8081 --profiles-dir /app/.dbt --project-dir /app/dbt',
        trigger_rule='all_done'
    )

    serve_docs_task
