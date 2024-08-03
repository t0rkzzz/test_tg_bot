# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ="Europe/Moscow"
COPY ./poetry.lock ./pyproject.toml /usr/src/app/

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN python -m pip install 'poetry==1.8.3'
RUN poetry install

COPY . .

CMD poetry run python main.py
