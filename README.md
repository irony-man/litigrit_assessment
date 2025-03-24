# PDF summary using Gemini API
A web app that quickly extracts and summarizes text from PDF files using the [Gemini LLM API](https://ai.google.dev/gemini-api/docs#python).

Designed for efficiency, it helps users save time by turning long documents into concise, easy-to-read summaries. Built with Django, PostgreSQL, and a sleek Bootstrap frontend, it is the perfect tool for professionals and students who need fast insights from PDFs.

Users can also see the chat history.

## Requirements  (Prerequisites)
Tools and packages required to successfully install this project.
* Linux
* Python 3.13
* Postgres 14

## Local Run Setup
### Set up postgres database
```
sudo -u postgres
\password your_password
CREATEDB db_name;
```
Clone the repo and run the following commands:
### Create a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Set up env variables
```
cat .env.template > .env
```
Add your variables to .env file


### Get Gemini API Key
You can get your API Key from [here](https://aistudio.google.com/apikey)

### Make migrations and migrate
```
python manage.py makemigrations
python manage.py migrate
```

### Create a superuser
```
python manage.py createsuperuser
```

### Run the server
```
python manage.py runserver
```

## Tech Stack / Built With
[Django](https://www.djangoproject.com/) - The Python framework
