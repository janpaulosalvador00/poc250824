import os
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import timedelta

# Definições dos parâmetros padrão e configuração do DAG
default_args = {
    'owner': 'Jan_Salvador_1014',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dbt_test',
    default_args=default_args,
    schedule_interval=None,  # DAG sem agendamento; será executada manualmente
    start_date=days_ago(1),  # Data no passado para garantir que a DAG possa ser executada manualmente
    catchup=False,  # Evita execução retroativa
    tags=['raw', 'trusted'],
) as dag:

    # Tarefa de início
    start = DummyOperator(
        task_id='start'
    )
    
    # Tarefa de fim
    end = DummyOperator(
        task_id='end'
    )

    # Grupo de tarefas relacionadas ao Airbyte
    with TaskGroup("airbyte_tasks") as airbyte_group:
        # Aciona a sincronização assíncrona com Airbyte
        async_money_to_json = AirbyteTriggerSyncOperator(
            task_id='airbyte_async',
            airbyte_conn_id='airbyte',
            connection_id='0d920354-9a07-493b-afb0-6a0c145b38bd',
            asynchronous=True,
        )

        # Sensor para monitorar o trabalho do Airbyte
        airbyte_sensor = AirbyteJobSensor(
            task_id='airbyte_sensor',
            airbyte_conn_id='airbyte',
            airbyte_job_id=async_money_to_json.output
        )

        # Definindo a ordem de execução dentro do grupo Airbyte
        async_money_to_json >> airbyte_sensor

    # Grupo de tarefas relacionadas ao DBT
    with TaskGroup("dbt_tasks") as dbt_group:
        # Comando para rodar 'dbt debug' para verificar a configuração
        dbt_debug = BashOperator(
            task_id='dbt_debug',
            bash_command='cd /path/to/dbt/project && dbt debug'
        )

        # Comando para rodar 'dbt run' após o Airbyte sync
        dbt_run = BashOperator(
            task_id='dbt_run',
            bash_command='cd /path/to/dbt/project && dbt run'
        )

        # Definindo a ordem de execução dentro do grupo DBT
        dbt_debug >> dbt_run

    # Definindo a ordem de execução entre os grupos e as tarefas finais
    start >> airbyte_group >> dbt_group >> end
