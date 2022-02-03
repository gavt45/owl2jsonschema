FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

ENV OWL_DB http://localhost:3030/test
ENV OWL_DB_TYPE turtle
ENV UPDATE_INTERVAL 10

RUN apk --update add bash nano

COPY ./requirements.txt /app/requirements.txt
COPY server.py /app/main.py
COPY owl2jsonschema.py /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt