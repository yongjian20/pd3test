#ARG APP_IMAGE=python:3.9
ARG DB_HOST
ARG DB_NAME
ARG DB_PASS
ARG DB_PORT
ARG DB_USER
ARG DEBUG
ARG PEPPER
ARG SECRET_KEY
ARG SENDGRID_API_KEY
ARG SENDGRID_EMAIL


#FROM $APP_IMAGE AS base

#FROM base as builder

FROM ubuntu
MAINTAINER Qxf2 Services
 
# Essential tools and xvfb
RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb \
	wget 
 
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99
 
# Firefox browser to run the tests
RUN apt-get install -y firefox
 
# Gecko Driver
#ENV GECKODRIVER_VERSION 0.23.0
#RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
#  && rm -rf /opt/geckodriver \
#  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
#  && rm /tmp/geckodriver.tar.gz \
#  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
#  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
#  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver \
#  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires
 
# python
RUN apt-get update && apt-get install -y \
    python 3.9\
    python-setuptools \
    python3-pip


RUN mkdir /project
WORKDIR /project

COPY requirements.txt /requirements.txt


RUN pip3 install -r /requirements.txt
ENV FLASK_APP app.py

COPY app.py  /project
ADD jenkins /project/jenkins/
ADD templates/ /project/templates/
ADD test /project/test/
ADD classes /project/classes
ADD static /project/static
RUN ls -laR /project

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8081"]
