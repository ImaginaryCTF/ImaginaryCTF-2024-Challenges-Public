FROM ubuntu:22.04

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update && apt-get -y install ruby nginx
RUN gem install sinatra
RUN gem install rackup

COPY app /app
RUN chmod +x /app/run.sh
COPY conf/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["/app/run.sh"]
