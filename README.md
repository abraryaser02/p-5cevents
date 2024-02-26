# Welcome to p-5cevents!

## Overview

p-5cevents is a full-stack web app with a Flask backend running on a Postgres database with React on the front-end. We will be dockerizing our app as we build it and have it production-ready using Gunicorn, Nginx, and DigitalOcean.

## Process

Currently, the app is at its basic stages. We have a small flask API endpoint set at `http://localhost:5001/users/ping` which displays
```
{
  "message": "pong!",
  "status": "success"
}
```
on your webpage!

To run docker and see this state-of-the-art website in use, follow this step:

```
docker-compose -f docker-compose-dev.yml up -d --build
```
The beauty of Docker is that you do not need to download any dependencies on your local machine for the website to pop up on your browser. You can run this command to bring up the Docker container and build the images (which in our case is users-db and users) and everything should work!

To recreate the database you can run the following command:

```
docker-compose -f docker-compose-dev.yml \
  run users python manage.py recreate_db
```
This command recreates our PostgreSQL database using `manage.py`, where we can define custom CLI (Command Line Interface) using Flask-CLI. In short, you can create your own fun commands and tell docker what to do! In this case, we are just telling it to re-create our database for us.

## More Database fun!

You can run the following command after recreating the database. This should connect you to Postgres' command line interface **psql**!
```
$ docker exec -ti $(docker ps -aqf "name=users-db") psql -U postgres

# \c users_dev
You are now connected to database "users_dev" as user "postgres".

# \dt
  List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

# \q 
```
If you are versed in SQL, you can also play around with it!
