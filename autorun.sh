#!/bin/sh
screen -d -m python3.10 /home/Portal/mainportal/manage.py runserver 0.0.0.0:9000 &
screen -d -m redis-server &
sleep 5 &&
cd mainportal/ && screen -d -m celery -A mainportal worker --loglevel=info &
cd mainportal/ && screen -d -m celery -A mainportal beat --loglevel=info
