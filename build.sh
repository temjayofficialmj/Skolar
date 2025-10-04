#!/usr/bin/env bash
set -euo pipefail

#!/usr/bin/env bash
set -e

# install deps (Render may already do this, but explicit is safer)
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# run migrations
python manage.py migrate --no-input

# wait for db (same pattern as above)...
python wait_for_db.py

# then start gunicorn/daphne/uvicorn
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
