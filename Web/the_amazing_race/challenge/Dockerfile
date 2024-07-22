FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip3 install flask Flask-Limiter gunicorn

COPY . /app

RUN chmod -R 777 /app

USER 1000:1000

VOLUME /tmp
CMD gunicorn -w 8 -b 0.0.0.0:8000 app:app
