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
    'owner': 'Jan_Salvador_1805',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='raw_trusted',
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
            connection_id='49ecc1ff-791d-474c-a1c3-11ed6ec494fc',
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
            #bash_command='cd /app/dbt && dbt debug'
            bash_command='dbt debug'
        )

        # Comando para rodar 'dbt run' após o Airbyte sync
        dbt_run = BashOperator(
            task_id='dbt_run',
            #bash_command='cd /app/dbt && dbt run'
            bash_command='dbt run'
        ) 

        # Generate the documentation files
        dbt_docs_generate = BashOperator(
            task_id='dbt_docs_generate',
            bash_command='dbt docs generate'
        )
        #it uses the port 8080 but since Airflow is using this port, you can point it to
        dbt_docs_serve_port = BashOperator(
            task_id='dbt_docs_serve_port',
            bash_command='dbt docs serve --port 8081'
        )

        # Definindo a ordem de execução dentro do grupo DBT
        dbt_debug >> dbt_run >> dbt_docs_generate >> dbt_docs_serve_port


    # Definindo a ordem de execução entre os grupos e as tarefas finais
    start >> airbyte_group >> dbt_group >> end
