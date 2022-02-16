FROM python:3.9-slim-buster

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN apt install -y netcat-openbsd && pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && rm -rf /root/.cache/pip

COPY . /app
WORKDIR /app

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]