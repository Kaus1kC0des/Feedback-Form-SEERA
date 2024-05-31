FROM python:3.10

# Accept the SQLALCHEMY_DATABASE_URI as a build argument
ARG SQLALCHEMY_DATABASE_URI

# Set environment variables
ENV SQLALCHEMY_DATABASE_URI=$SQLALCHEMY_DATABASE_URI

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir pipenv
RUN pipenv install --deploy --ignore-pipfile

EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app

LABEL authors="kausik"