from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount

# this is to use python and bash in airlflow
from airflow.operators.python import PythonOperator
# from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}


def run_elt_script():
    # the script points to the docker container
    script_path = "/opt/airflow/elt_script/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    # this is control code to rais error is script dosent run successfullu
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag = DAG(
    'elt_and_dbt',                     # Name of the dag
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2024, 3, 30),  # date of when this was run
    catchup=False,
)

# this task is for elt_script
t1 = PythonOperator(
    task_id='run_elt_script',
    python_callable=run_elt_script,
    dag=dag,
)

# this is for DBT
# the info we previously added in docker-compose can be added here
t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir", "/root",
        "--project-dir", "/opt/dbt",
        "--full-refresh"
    ],
    auto_remove=True,   # do we want to automatically remove the container after its done
    docker_url="unix://var/run/docker.sock",  # the socket we opened (in docker-compose) for airflow to control docker 
    network_mode="bridge",
    mounts=[
        Mount(source='c/Users/Mahum/Desktop/Projects/DE_YT/ELT_project', # the path of your folder in Unix format
              target='/opt/dbt', type='bind'),
        Mount(source='c/Users/Mahum/.dbt', target='/root', type='bind'),
    ],
    dag=dag
)

# create the order in which we want the tasks to run
t1 >> t2