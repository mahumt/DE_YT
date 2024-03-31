FROM python:3.8-slim

# RUN command to install postgress sql command line tools
# this command line functionality will be used in the elt_script.py 
# to dump and load data from destination to source DB
RUN apt-get update && apt-get install -y postgresql-client 

# # Run command for postgres and crom. comment out the above run command
# RUN apt-get update && apt-get install -y postgresql-client cron

# this copies the cron job into the app driectory of docker
# COPY start.sh /app/start.sh

# copy command to copy over the script in docker
COPY elt_script.py .

# set the working directory
# WORKDIR /app

# running the cron job at 1:22 am 
# RUN echo " 0 1 2 5 * python /app/elt_script.py" | crontab -

# cmd to specfiy default system and file to runs
CMD ["python", "elt_script.py"]