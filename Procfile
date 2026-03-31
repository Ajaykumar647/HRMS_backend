web: python manage.py migrate && gunicorn hrms.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --log-file -
