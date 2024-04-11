FROM python:3.11-slim
LABEL maintainer="pcngumoha"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

EXPOSE 8000

WORKDIR /app

RUN set -x && apt update && \
  apt install -y --no-install-recommends libpq-dev libpq5 gcc python3.11-dev && \
  python -m venv /env && \
  /env/bin/pip install --upgrade pip && \
  /env/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
  /env/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt && \
  adduser --disabled-password --no-create-home dev-user && \
  apt purge -y --auto-remove gcc libpq-dev && \
  rm -rf /tmp

ENV PATH="/env/bin/:$PATH"

USER dev-user
