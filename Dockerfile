FROM python:3.7

RUN mkdir /app

COPY src /app
WORKDIR app
