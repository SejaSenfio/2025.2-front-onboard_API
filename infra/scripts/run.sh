#! /bin/bash

echo "$(date +"%d/%m/%Y %H:%M:%S") | Checking Database Connection 🟡 ($DB_HOST:$DB_PORT/$DB_NAME) 🟡"
while ! nc -z $DB_HOST $DB_PORT; do
    echo "$(date +"%d/%m/%Y %H:%M:%S") | ⌛ Waiting... "
    sleep 2
done

echo "$(date +"%d/%m/%Y %H:%M:%S") | ---> Database Connection Established ✅"

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "$(date +"%d/%m/%Y %H:%M:%S") | Running Migrations 🐍"
    python3 /app/src/manage.py migrate
    python3 /app/src/manage.py devsetup
    echo "$(date +"%d/%m/%Y %H:%M:%S") | ---> Migrations ran successfully ✅"
fi

echo "$(date +"%d/%m/%Y %H:%M:%S") | 🚀🏁 Starting App in ${APP_RUN_PORT:-8000}..."
gunicorn --workers="${GUNICORN_WORKERS:-4}" --timeout "${REQUEST_TIMEOUT:-120}" --log-level "${LOG_LEVEL:-INFO}" -b 0.0.0.0:"${APP_RUN_PORT:-8000}" config.wsgi:application