# syntax=docker/dockerfile:1

FROM mysql:latest

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get install unzip \
    && apt-get install -y wget \
    && wget -N https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip -P ~/Downloads \
    && unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads \
    && chmod +x ~/Downloads/chromedriver \
    && mv -f ~/Downloads/chromedriver /usr/local/share/chromedriver

WORKDIR /usr/bin/chromedriver

RUN ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
    && ln -s /usr/local/share/chromedriver /usr/bin/chromedriver \
    && apt-get clean \
    && chown root:root /usr/local/bin/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver

WORKDIR /app
COPY . .
RUN pip3 install -r ./instance/requirements.txt
CMD docker-entrypoint.sh mysqld & \
    python3 Scrapers/WebScraperMain.py & \
    cd /app/src \
    && flask run --host=0.0.0.0;