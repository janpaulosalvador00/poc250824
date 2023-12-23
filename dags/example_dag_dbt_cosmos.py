"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

# from cosmos import DbtTaskGroup, ProjectConfig, RenderConfig
# from cosmos.constants import TestBehavior
from pendulum import datetime

# from include.constants import DBT_PROJECT_PATH, venv_execution_config
# from include.profiles import postgres_config

POSTGRES_CONN_ID = "dev-postgres"
# DB_NAME = "dbt_dev"
# SCHEMA_NAME = "dbt_example"
# MODEL_NAME = "my_first_dbt_model"
DB_NAME = "defaultdb"
SCHEMA_NAME = "public"
MODEL_NAME = "books"

with DAG(
    dag_id="example_dag_dbt_cosmos",
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
) as dag:
    # starters = DbtTaskGroup(
    #     group_id="starters",
    #     project_config=ProjectConfig(DBT_PROJECT_PATH),
    #     profile_config=postgres_config,
    #     execution_config=venv_execution_config,
    #     render_config=RenderConfig(
    #         select=["my_first_dbt_model"], test_behavior=TestBehavior.NONE
    #     ),
    # )

    query_table = PostgresOperator(
        task_id="query_table",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"SELECT * FROM {DB_NAME}.{SCHEMA_NAME}.{MODEL_NAME} LIMIT 5",
    )

# starters >> query_table
query_table
