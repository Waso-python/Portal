# Portal

source venv/bin/activate 
python3 manage.py runserver

pip3 freeze > requirements.txt


python3 manage.py migrate

python3 manage.py makemigrations

python3 manage.py migrate 


superuser - sdarr, pass - 123