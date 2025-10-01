#!/usr/bin/env bash
set -euo pipefail

# install deps (Render may already do this, but explicit is safer)
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# run migrations
python manage.py migrate --no-input
