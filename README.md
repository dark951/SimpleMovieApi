# Welcome in 'SimpleMovieApi' recruiting exercise

## setting up

### just run this commands

1. pip install -r requirements.txt
2. sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common

3. sudo -i -u postgres
4. createuser postgersUser -P --interactive
5. password 'pass'
6. createdb postgersbd

### configure OMDBAPI token

1. go here **http://www.omdbapi.com/apikey.aspx**
2. get your own api key
3. paste key in **SimpleMovieApi/settings.py** as a value of OMDBAPI_API_KEY

## usage

### to run server use:

python manage.py runserver

### to run tests use:

python manage.py test

### to make and run migrations use

python manage.py makemigrations

and 

python manage.py migrate


`Be blessed!`
