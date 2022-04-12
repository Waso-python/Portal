# Portal
# Django based system for monitoring trade operation on federal portals
pip3 install psycopg2-binary


source venv/bin/activate 
python3 manage.py runserver

pip3 freeze > requirements.txt


python3 manage.py migrate

python3 manage.py makemigrations

python3 manage.py migrate 

python manage.py createsuperuser
superuser - sdarr, pass - 123