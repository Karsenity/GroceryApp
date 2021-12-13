# syntax=docker/dockerfile:1

FROM mysql:latest
#FROM python:3.10.1

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean

WORKDIR /app
COPY ../.. .
RUN pip3 install -r requirements.txt
RUN [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "&"]
WORKDIR "./src"

# mysql -u root -ppassword
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]