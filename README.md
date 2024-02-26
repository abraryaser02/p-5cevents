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
If you are versed in SQL, you can also play around with it! # indicates that we are inside the psql shell.
After you login using the previous command, you can play around with psql!

```
postgres=# \c users_dev
You are now connected to database "users_dev" as user "postgres".

users_dev=# select * from users;
 id | username | email | active
----+----------+-------+--------
(0 rows)

users_dev=# INSERT INTO users (username, email, active) VALUES ('abrar', 'abrar@pomona.edu', true);
INSERT 0 1
users_dev=# select * from users;
 id | username |      email       | active
----+----------+------------------+--------
  1 | abrar    | abrar@pomona.edu | t
(1 row)

users_dev=# INSERT INTO users (username, email, active) VALUES
users_dev-# ('sae', 'sae@pomona.edu', true),
users_dev-# ('asya', 'asya@pomona.edu', true),
users_dev-# ('yunju', 'yunju@pomona.edu', true),
users_dev-# ('dylan', 'dylan@pomona.edu', true),
users_dev-# ('oncel', 'oncel@cmc.edu', true),
users_dev-# ('landen', 'landen@pomona.edu', true),
users_dev-# ('david', 'david@pomona.edu', true),
users_dev-# ('sadhvi', 'sadhvi@hmc.edu', true),
users_dev-# ('sumi', 'sumi@pomona.edu', true);
INSERT 0 9

users_dev=# select * from users;
 id | username |       email       | active
----+----------+-------------------+--------
  1 | abrar    | abrar@pomona.edu  | t
  2 | sae      | sae@pomona.edu    | t
  3 | asya     | asya@pomona.edu   | t
  4 | yunju    | yunju@pomona.edu  | t
  5 | dylan    | dylan@pomona.edu  | t
  6 | oncel    | oncel@cmc.edu     | t
  7 | landen   | landen@pomona.edu | t
  8 | david    | david@pomona.edu  | t
  9 | sadhvi   | sadhvi@hmc.edu    | t
 10 | sumi     | sumi@pomona.edu   | t
(10 rows)

// inserting a value by mistake
users_dev=# INSERT INTO users (username, email, active) VALUES ('abrar', 'abrar@pomona.edu', true);
INSERT 0 1

users_dev=# select * from users;
 id | username |       email       | active
----+----------+-------------------+--------
  1 | abrar    | abrar@pomona.edu  | t
  2 | sae      | sae@pomona.edu    | t
  3 | asya     | asya@pomona.edu   | t
  4 | yunju    | yunju@pomona.edu  | t
  5 | dylan    | dylan@pomona.edu  | t
  6 | oncel    | oncel@cmc.edu     | t
  7 | landen   | landen@pomona.edu | t
  8 | david    | david@pomona.edu  | t
  9 | sadhvi   | sadhvi@hmc.edu    | t
 10 | sumi     | sumi@pomona.edu   | t
 11 | abrar    | abrar@pomona.edu  | t
(11 rows)

// no worries, we can always delete it
users_dev=# DELETE from users WHERE username = 'abrar' and id = '11';
DELETE 1
users_dev=# select * from users;
 id | username |       email       | active
----+----------+-------------------+--------
  1 | abrar    | abrar@pomona.edu  | t
  2 | sae      | sae@pomona.edu    | t
  3 | asya     | asya@pomona.edu   | t
  4 | yunju    | yunju@pomona.edu  | t
  5 | dylan    | dylan@pomona.edu  | t
  6 | oncel    | oncel@cmc.edu     | t
  7 | landen   | landen@pomona.edu | t
  8 | david    | david@pomona.edu  | t
  9 | sadhvi   | sadhvi@hmc.edu    | t
 10 | sumi     | sumi@pomona.edu   | t
(10 rows)
```
