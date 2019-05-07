FROM python:3.7

ADD . /code
WORKDIR /code

RUN pip3 install --upgrade pip
RUN pip3 install -r web/requirements.pip

EXPOSE 8000

CMD ["python", "web/server.py"]
