FROM python:3-alpine

WORKDIR /app

RUN apk add --no-cache git

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install

COPY vesync.py .

CMD pipenv run python vesync.py
