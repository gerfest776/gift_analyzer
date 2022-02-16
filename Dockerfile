FROM python:3.9-slim-buster
#RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry
RUN poetry install

COPY . /app
WORKDIR /app

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]