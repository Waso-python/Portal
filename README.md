# Portal
# Django based system for monitoring trade operation on federal portals

stack: Djando, Celery, Postgres

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r requirements.txt

pip3 install django

pip3 install psycopg2-binary


source venv/bin/activate  python3 manage.py runserver

pip3 freeze > requirements.txt


python3 manage.py migrate

python3 manage.py makemigrations

python3 manage.py migrate 

python manage.py createsuperuser
superuser - , pass - 

в отдельном (в папке где лежит manage.py)
celery -A mainportal worker --loglevel=info

после в отдельном окне 
celery -A mainportal beat --loglevel=info
