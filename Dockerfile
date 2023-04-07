FROM python:3.9-slim

RUN mkdir /app

RUN apt-get update
RUN apt-get install -y gcc default-libmysqlclient-dev

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY stock_app/ /app

WORKDIR /app