FROM ubuntu:22.04

RUN apt update -y && apt install -y swi-prolog tmux
WORKDIR /app
COPY server.pl .
COPY run.sh /run.sh
RUN chmod +x /run.sh

VOLUME /tmp

EXPOSE 80
CMD /run.sh
