FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt