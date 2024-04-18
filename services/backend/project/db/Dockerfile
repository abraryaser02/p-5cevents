# pull official base image
FROM postgres:16

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d

# COPY ./requirements.txt ./

# RUN pip install -r requirements.txt
