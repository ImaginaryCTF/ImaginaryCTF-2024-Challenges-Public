FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev socat

RUN pip3 install console

WORKDIR /app

COPY . /app

RUN chmod -R 555 /app

CMD socat -dd TCP4-LISTEN:1337,fork,reuseaddr SYSTEM:./wrapper.sh,pty,echo=0
