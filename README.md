# Portal
# Django based system for monitoring trade operation on federal portals

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
pip3 install django

pip3 install psycopg2-binary


source venv/bin/activate 
python3 manage.py runserver

pip3 freeze > requirements.txt


python3 manage.py migrate

python3 manage.py makemigrations

python3 manage.py migrate 

python manage.py createsuperuser
superuser - sdarr, pass - 123
