# syntax=docker/dockerfile:1

FROM mysql:latest
#FROM python:3.10.1

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean

WORKDIR /app
COPY . .
RUN pip3 install -r ./instance/requirements.txt
WORKDIR ./src
CMD docker-entrypoint.sh mysqld & cd /app/src && flask run --host=0.0.0.0;


# mysql -u root -ppassword
