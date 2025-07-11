FROM alpine:latest

RUN apk update
RUN apk add --no-cache python3
RUN apk add --update py3-pip
RUN apk add --no-cache --upgrade bash

RUN python3 -m venv /home/py-env
RUN /home/py-env/bin/pip3 install psycopg2-binary

WORKDIR /home
