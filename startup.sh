#!/bin/sh
exec gunicorn -w 4 -b :5000 --access-logfile - --error-logfile - csaf:app
