FROM python:3.10.1-slim-buster

WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update \
        && apt-get -y install netcat gcc \
        && apt-get clean

RUN mkdir -p /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app .
