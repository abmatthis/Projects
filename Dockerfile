FROM python:3.10
WORKDIR /app

COPY flask_app server.py Pipfile /app/
RUN pip install pipenv 
RUN pipenv install
RUN pipenv shell

EXPOSE 5000


ENTRYPOINT pipenv run python server.py 