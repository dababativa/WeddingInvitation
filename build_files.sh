#!/usr/bin/env bash

echo "Building project requirements..."

python3 -m pip install -r requirements.txt
# python3 -m pip install sqlite-devel
python3 -m pip install libsqlite3-dev

echo "Migrating Database..."

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting Static Files..."
python3 manage.py collectstatic --noinput