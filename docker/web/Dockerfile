FROM python:3.7-alpine

RUN apk add --update alpine-sdk
RUN apk add libffi-dev openssl-dev

ADD . /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install -r web/requirements.pip
RUN [ "python", "-c", "import nltk; nltk.download('all')" ]
