FROM python:3.10-slim

WORKDIR app/
RUN apt update && apt install -y gcc libpq-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
CMD python manage.py runserver 0.0.0.0:8000 --noreload