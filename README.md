# PDF summary using Gemini API
A web app that quickly extracts and summarizes text from PDF files using the [Gemini LLM API](https://ai.google.dev/gemini-api/docs#python).

Designed for efficiency, it helps users save time by turning long documents into concise, easy-to-read summaries. Built with [Django](https://www.djangoproject.com/), [PostgreSQL](https://www.postgresql.org/), and a sleek [Bootstrap](https://getbootstrap.com/) and [jQuery](https://jquery.com/) frontend, it is the perfect tool for professionals and students who need fast insights from PDFs.

Users can also see the chat history. Using django session, we non logged in users can also see their history. Users can also see a particular summary with extracted text and summary and title we got from Gemini API.

[Django template](https://docs.djangoproject.com/en/5.1/topics/templates/) has been used for front-end which is rendered from Django back-end although I have [Django Rest Framework](https://www.django-rest-framework.org/) at some places (Summary Post) to showcase my skills.

## Requirements  (Prerequisites)
Tools and packages required to successfully install this project.
* Linux
* Python 3.13
* Postgres 14

## Local Run Setup
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

### Set up postgres database
1. Create a Database in Postgres
    ```
    sudo -u postgres
    \password your_password
    CREATEDB db_name;
    ```
2. Add database keys to `.env` file
    ```
    POSTGRES_HOST=your_db_host
    POSTGRES_DATABASE=your_db_name
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_PORT=your_db_port
    ```

### API Key Instructions
1. Visit the [Gemini API Key page](https://aistudio.google.com/apikey).
2. Generate a new API key.
3. Add the key to your `.env` file:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

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
* [Django](https://www.djangoproject.com/) - The Python framework
* [PostgreSQL](https://www.postgresql.org/) - The database management system
* [Bootstrap](https://getbootstrap.com/) - The frontend framework

## Future Enhancements
1. Add support for additional file formats (e.g., Word documents).
3. Introduce advanced summarization options, such as keyword-based summaries.
4. Optimize performance for large PDF files.
