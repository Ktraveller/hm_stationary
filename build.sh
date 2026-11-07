#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

test -f staticfiles/login.css
test -f staticfiles/customer_css/dashboard.css
test -f staticfiles/customer_js/dashboard.js
test -f staticfiles/stationary_css/stationary.css
test -f staticfiles/stationary_js/activity.js
