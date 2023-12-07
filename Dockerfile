FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/parser

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY django_admin /usr/parser/django_admin
COPY src /usr/parser/src
