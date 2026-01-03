#!/bin/bash
set -e

# Ensure we run from the Django project directory (manage.py is in app_financeiro/)
APP_DIR="/app/app_financeiro"
if [ -d "$APP_DIR" ]; then
  cd "$APP_DIR"
fi

# Apply database migrations, collectstatic and start server
python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true

# Start Gunicorn (module path is app_financeiro.wsgi when started from APP_DIR)
exec gunicorn app_financeiro.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --log-level ${GUNICORN_LOG_LEVEL:-info}
