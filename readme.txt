1) Install Python 3.7
2) Install Postgresql
3) Install pgadmin4
4) Create database sensai in pgadmin4
5) Create virtual envirment 'python -m venv venv'
6) Activate venv '.\venv\Scripts\activate.bat'
7) Install required packages 'pip install -r requirements.txt'
8) Make migrations for DB 'python manage.py makemigrations'
9) Add migrations to DB 'python manage.py migrate'
10) Run 'python manage.py createsuperuser' for creating superuser chose email and password
11) Run the Server 'python manage.py runserver ' creates local Host by default port 8000
12) Open Chrome or whatever browser you want search localhost:8000 or 127.0.0.1:8000
13) Open localhost:8000/admin/ and login with your data
