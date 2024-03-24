## Introduction
This exercise takes data from one source folder and moves it across to a destination folder. <br>
We use a CRON job to let it <br>
We use Airflow for <br>
We use Airbyte for <br>
And, lastly we use dbt (data build tool) on top of the destination data for transformation <br> 

## How it works/Repository Structure
docker-compose.yaml: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines three services:

source_postgres: The source PostgreSQL database.
destination_postgres: The destination PostgreSQL database.
elt_script: The service that runs the ELT script.
elt_script/Dockerfile: This Dockerfile sets up a Python environment and installs the PostgreSQL client. It also copies the ELT script into the container and sets it as the default command.

elt_script/elt_script.py: This Python script performs the ELT process. It waits for the source PostgreSQL database to become available, then dumps its data to a SQL file and loads this data into the destination PostgreSQL database.

source_db_init/init.sql: This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables.

How It Works
Docker Compose: Using the docker-compose.yaml file, three Docker containers are spun up:

A source PostgreSQL database with sample data.
A destination PostgreSQL database.
A Python environment that runs the ELT script.
ELT Process: The elt_script.py waits for the source PostgreSQL database to become available. Once it's available, the script uses pg_dump to dump the source database to a SQL file. Then, it uses psql to load this SQL file into the destination PostgreSQL database.

Database Initialization: The init.sql script initializes the source database with sample data. It creates several tables and populates them with sample data.

## Dependencies:
    Docker Desktop and Docker Compose
    Airflow from Docker
    DBT downloaded through Python's pip. 
        Make sure there is a ''' .dbt ''' folder in the home directory
            ''' 
            $ mkdir $home\.dbt 
            '''
        I did this in a virtual environment (dbt-env) created in the main folder (FolderA)
        '''
        python -m pip venv dbt_env
        ./dbt_env/Scripts/activate.bat
        python -m pip install dbt-postgres
        dbt init
        '''

## Getting Started
    Either clone the respository and start '''docker-compose up'''
OR <br>
    - Create a folderA <br>
    - Docker-compose.yaml <br>
    - Inside folderA create Folder called "elt" and add Dockerfile and elt_script.py in it. <br>
    - Navigate to FolderA using terminal and run  <br>
    '''
    docker-compose up
    '''
<br>
Once all containers are up and running, the ELT process will start automatically. <br>
After the ELT process completes, you can access the source and destination PostgreSQL databases on ports 5433 and 5434, respectively. <br>