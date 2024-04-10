FROM python:3.11-slim
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

EXPOSE 8000

WORKDIR /app

RUN python -m venv /env && \
  /env/bin/pip install --upgrade pip && \
  /env/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
  /env/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt && \
  adduser --disabled-password --no-create-home dev-user && \
  rm -rf /tmp

ENV PATH="/env/bin/:$PATH"

USER dev-user
