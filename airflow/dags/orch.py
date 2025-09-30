from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator

import sys
sys.path.append('/opt/airflow/src')
from connection import main


def get_weather_data():
    return main()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

dag = DAG(
    dag_id='my_test_dag',
    default_args= default_args,
    schedule=timedelta(minutes=1)
)

with dag:

    task1 = PythonOperator(
        task_id = "weather_data_ingestion",
        python_callable = get_weather_data
    )


    task2 = DockerOperator(
        task_id = "transform_data",
        image = "ghcr.io/dbt-labs/dbt-postgres:1.9.latest",
        command = "run",
        working_dir = "/usr/app",
        mounts = [
            Mount(source='/home/isho/data/weather_airfolw_project/dbt/my_dbt',
                  target='/usr/app',
                  type='bind'
                  ),
            Mount(source='/home/isho/data/weather_airfolw_project/dbt/profiles.yml',
                  target='/root/.dbt/profiles.yml',
                  type='bind'),
        ],
        network_mode="my-network",
        docker_url = "unix://var/run/docker.sock",
        auto_remove = 'success'
    )

    task1 >> task2



