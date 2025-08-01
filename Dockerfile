FROM python:3.12

WORKDIR /e2ee

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python manage.py makemigrations app && \
    python manage.py migrate app && \
    daphne -b 0.0.0.0 -p 8080 config.asgi:application
