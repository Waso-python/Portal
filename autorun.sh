#!/bin/sh
screen -L python3.10 home/Portal/mainportal/manage.py runserver &
screen -L redis-server &
sleep5 &&
cd mainportal/ && screen -L celery -A mainportal worker --loglevel=info &
screen -L celery -A mainportal beat --loglevel=info
