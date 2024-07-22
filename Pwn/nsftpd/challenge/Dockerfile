FROM ubuntu:22.04

RUN /usr/sbin/useradd -u 1000 user

COPY flag.txt /
RUN chmod 000 /flag.txt

COPY getflag /
RUN chown root:root /getflag
RUN chmod 755 /getflag
RUN chmod +s /getflag

COPY ./ftp_project/ftpd/ftpd /home/user/ftpd
RUN chmod +x /home/user/ftpd
RUN chmod 777 /home/user/

EXPOSE 1337
WORKDIR /home/user/
USER user

CMD ["./ftpd", "1337"]
