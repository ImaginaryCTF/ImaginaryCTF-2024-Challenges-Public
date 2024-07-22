FROM python:3.9-slim

ENV FLASK_APP=/app/app.py:app

RUN pip install flask==3.0.3

WORKDIR /app
COPY app.py /app/app.py
COPY flag.txt /app/flag.txt
COPY templates/ /app/templates/

EXPOSE 80


WORKDIR /app
CMD ["python3", "/app/app.py"]
