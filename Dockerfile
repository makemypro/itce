# syntax=docker/dockerfile:1
FROM python:3

# Env set
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /code

# Update pip

RUN pip install --upgrade pip

# Install requirements
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/