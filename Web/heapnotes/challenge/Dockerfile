FROM python:3.9-slim

ENV FLASK_APP=/app/app.py:app

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY app.py /app
COPY flag.txt /app/flag.txt
COPY templates/ /app/templates/
COPY ssl/ /app/ssl/

EXPOSE 80

VOLUME /tmp

CMD ["python3", "/app/app.py"]
