# Data engineering Pipeline
## Table of contents
- [Introduction](#introduction)
- [How it works/Repository Structure](#how-it-worksrepository-structure)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Working exercise: commands and screenshots](#working-exercise-commands-and-screenshots)
- [Limitations of this exercise](#limitations-of-this-exercise)
- [Push project remotely just using Github and Vscode](#push-project-remotely-just-using-github-and-vscode)
- [Source](#source)

## Introduction
This exercise takes data from one source folder and moves it across to a destination folder. <br>

### Tools and their uses
- A `CRON` job: A `.sh` file to run the pipeline at a specific time. This is in essence a less detailed version of what airflow will do. But good to learn none-the-less since companies do use these.  <br>
- `Airflow` for scheduling of the pipeline. Using DAGs (Directed Acyclic Graphics). This will help us run the pipeline on a schedule automatically.  <br>
- `dbt` (data build tool) on top of the destination data for transformations to the data. Focusing on models and macros, but dbt can also run tests on the transformation for a robust pipeline <br> 

## How it works/Repository Structure
1. docker-compose.yaml: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines three services: <br>
i. `source_postgres:` The source PostgreSQL database with sample data. <br>
ii. `destination_postgres:` The destination PostgreSQL database where the pipeline will dump data. <br>
iii. `elt_script.py:` The service that runs the ELT script, in a python envionment. The elt_script.py waits for the source PostgreSQL database to become available. Once it's available, the script uses pg_dump to dump the source database to a SQL file. Then, it uses psql to load this SQL file into the destination PostgreSQL database.<br>
2. `elt_script/Dockerfile:` This Dockerfile sets up a Python environment and installs the PostgreSQL client. It also copies the ELT script into the container and sets it as the default command. <br>
3. `elt_script/elt_script.py:` This Python script performs the ELT process. It waits for the source PostgreSQL database to become available, then dumps its data to a SQL file and loads this data into the destination PostgreSQL database. <br>
4. `source_db_init/init.sql:` This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables. <br>

## Dependencies:
0. It is better to do this entire exercise in a virtual environement. I named mine `dbt_env` after the usage of venv specfically for dbt installation. To create environment `python -m pip venv dbt_env ` <br>
To activate the environemt (venv) `.\dbt_env\Scripts\activate`
To freeze the environment's packages use `python -m pip freeze > Requirements.txt` <br>
To recreate the environment with the same package `python -m pip install -r .\ requirements. txt.` <br>
1. Docker Desktop and Docker Compose <br>
2. DBT downloaded through Python's pip. <br> 
i. Make sure there is a `.dbt ` folder in the home directory; where the profiles.yml file will reside <br>
```$ mkdir $home\.dbt```
<br>
ii. I downloaded/installed dbt in a virtual environment (dbt-env) created in the main folder (FolderA)
```
python -m pip install dbt-postgres    # to install dbt in the venv, this will add a dbt.exe in Scripts folder of the venv
dbt init                              # since we have the dbt.exe in the scripts folder we can run this using CLI
```
<br>
iii. For first time user no profile.yml file exists. So dbt will ask everything in terminal to create one. From next time onward the file can be edited for adding/deleting projects. <br>
For Windows use
`notepad $home/.dbt/profiles.yml` <br>
Information asked will be: <br>

```
Enter a number: 1
host (hostname for the instance): host.docker.internal
port [5432]: 5434
user (dev username): postgres
pass (dev password):
dbname (default database that dbt will build objects in): destination_db
schema (default schema that dbt will build objects in): public
threads (1 or more) [1]: 1
``` 
iv. In the dbt's project folder, open the file `dbt_project.yml` and change `+materialized` to `table` from `view`. Materialization is a variable that controls how dbt creates a model, wfor this purpose we want to use our tables. <br>
v. In the models folder, add sources/references `actors.sql`, `film_actors.sql`, `films.sql` and then define the schema from `schema.yml`. The schema file is useful in testing. When dbt runs the test it will use this file as reference and if the schema does not match throw errors <br>
<br>
3. Scheduling using CRON job <br>
When we are using CRON to schedule our job in the `./elt/Dockerfile`  we will add `run CRON` `copy to docker directory` `define working directory` and `run echo cron at a specific datetime`  commands. <br>
<br>
4. Scehduling using Airflow from Docker <br>
When we are using Airflow instead of CRON we need to comment out our elt_script and dbt images in docker-compose. That can be now found in our `./airflow/dags/elt_dag.py` folder instead. We can also go in `./elt/Dockerfile` and comment out `run` `copy` `workdir` `run echo` commands. <br>
We need to rund the airflow init container first and then in a new terminal open up airflow UI by using `docker compose up init-airflow -d`. Whic initalizes airflow and exits with code 0 (i.e. successful) after setting it up
<br>
This is a one time thing. Next time just run the airflow init command first and then `docker compose up` in a different terminal


## Getting Started
Either clone the respository and start `docker-compose up` <br>
OR <br>
    - Create a folderA <br>
    - Create Docker-compose.yaml <br>
    - Inside folderA create Folder called "elt" and add Dockerfile and elt_script.py in it. <br>
    - Navigate to FolderA using terminal and run  `docker-compose up`
<br>
Once Container with all images are up and running, the ELT process will start automatically. <br>
After the ELT process completes, you can access the source and destination PostgreSQL databases on ports 5433 and 5434, respectively. (see next section for commands)<br>


## Working exercise: commands and screenshots
- Screenshot of destination and source folder/postgtress being created in powershell
![Screenshot of destination and source folder/postgres being created in powershell.](./Screenshot_1.png)
Use command in new terminal: 
```
docker exec -it de_yt-destination_postgres-1 psql -U postgres
\c destination_db   # \c is for connecting to database
\dt
```
1 - Screenshot of postgress tables created script running successfully <br>
![Screenshot of postgress destination tables](./postgres_db.png)

2 - Screenshot of elt script running successfully <br>
![Screenshot of elt script running successfully](./Screenshot_2.png)

3 - Screenshot of dbt transformations <br>
![Screenshot of dbt transformations](./Screenshot_3.png)

4 - Screenshot of portgres tables after dbt transformations run <br>
![Screenshot of postgres after dbt transformation](./postgres_after_dbt.png)

5 - Screenshot running airflow first time <br>
![running airflow](<./running_airflow_first _time.png>)

6 - Screenshot of running docker command to start airflow `docker compose up init-airflow -d`<br>
![docker command to run airlofw](docker_command_to_run_airflow.png)

7- Screenshot of successful dag run within airflow <br>
![successful dag run](./sucessful_dag_run.png)

8 - Screenshot of successful table creation using airflow <br>
![airflow tables](airflow_tables.png)

## Limitations of this exercise
- This exercise is very basic. Most real life jobs will not require moving data from one folder to another on-prem.
- Exercises like this will also not use the same schema in both source and destination databases.
- This exercise uses a varitation of batch system. But in most cases data will be too big to for this to work efficently.
    - The way to improve upon this exercise is to add cloud services and more open source tools for batch processing using "Spark" and Stream processings using "Kafka".
    - There can be multiple sources for data
    - Data should also be first stored in a staging area and then move into data warehouses, becuase in the future revert or backfilling might be needed
    - To make it completely end-to-end the data should be used in a model that is deployed as part of a site or transformations can be used to gain insights and make strategic decisions using data visualisation tools. 

## Push project remotely just using Github and Vscode
Open terminal in Vscode
```
git remote -v 
git remote add origin https://github.com/<user>/<user_repository>
git add .
git commit -m "updates to schema and sql files"
git push origin main
```

## Source
https://www.youtube.com/watch?v=PHsC_t0j1dU&list=WL&index=14&ab_channel=freeCodeCamp.org