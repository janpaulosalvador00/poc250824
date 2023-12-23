import os

from cosmos import ExecutionConfig

DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt"

venv_execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)
