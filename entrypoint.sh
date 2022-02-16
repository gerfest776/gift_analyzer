#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z database 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py migrate

echo "
O——————————————————O
     Gift Analyzer started…
O——————————————————O
"
exec "$@"