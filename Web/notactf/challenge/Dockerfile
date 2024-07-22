FROM mongo:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update; apt-get -y install python3 python3-pip

ENV MONGO_INITDB_DATABASE main

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

COPY run.sh /run.sh
RUN chmod +x /run.sh

VOLUME /tmp

CMD ["/run.sh"]
