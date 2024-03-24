FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client
#RUN command to install postgress sql command line tools
# this command line functionality will be used in the elt_script.py 
# to dump and load data from destination to source DB

COPY elt_script.py .
# copy command to copy over the script in docker

CMD ["python", "elt_script.py"]
# cmd to specfiy default system and file to runs