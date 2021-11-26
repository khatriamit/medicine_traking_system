# For API docs

after successfully setting up the project
```sh
In your browser ##localhost:8000/docs/
If it did not work at first press Ctrl+ s in your api/main.py 
```

# FastAPI in Docker


## Git

Clone this repository
```sh
$ git clone https://github.com/pydevnepal/medicine_traking_system.git
```
## Docker
Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) in your system.
Create a local copy of `docker-compose.local.yml` on your machine.


## create image
$ docker build -t med/api:0.0.1 .


To run the project in docker

    $ docker-compose up -d			#  Will create all necessary services
    Starting med_db ... done
    Starting med_service   ... done


To stop all running containers

    $ docker-compose stop			# Will stop all running services
    Stopping med_db ... done
    Stopping med_service   ... done

## Check your database


    $ docker exec -it med_db psql -U postgres
    $ postgres=# \t                     # To check your table if medicine is in your list then your db is ready else follow the command below

## Create your database

    $ docker exec -it med_service bash
    $ root@<container_id>:/code# alembic upgrade head       # Then follow the check your database steps


## Postgresql
In case if you want to use a local postgresql server instead on running a docker container.
First verify if `postgresql` is installed.

     $ psql -V
     psql (PostgreSQL) 10.0
Edit `postgresql.conf` file to allow listening to other IP address.

    $ sudo nano /etc/postgresql/10/main/postgresql.conf
    listen_addresses = '*'          # what IP address(es) to listen on;
Now you will need to allow authentication to `postgresql` server by editing `pg_hba.conf`.

    $ sudo nano /etc/postgresql/10/main/pg_hba.conf

Find `host    all             all             127.0.0.1/32            md5`  and change it to `host    all    all    0.0.0.0/0    md5`

Restart your postgresql server.

    $ sudo systemctl restart postgresql.service
You will now need to set environment `POSTGRES_HOST`  your private IP address like following.

    POSTGRES_HOST=192.168.1.22 				# my local postgresql server ip address

For creating a postgresql `role` , `database` & enabling `extensions`.

    $ sudo su - postgres
    $ psql
    psql> CREATE DATABASE myproject;
    psql> CREATE USER myprojectuser WITH PASSWORD 'password';
    psql> GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
    psql> CREATE EXTENSION postgis;

for deleting the current psql database and creating new one

    docker stop med_service
    docker exec -it database_postgres psql -U postgres
    psql> create database p1;
    psql> \c p1;
    psql> drop database medicine;
    psql> create database medicine;
    psql> \c medicine;


