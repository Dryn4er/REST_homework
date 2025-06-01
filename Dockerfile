FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY=django-insecure-s2^ju^mhoq(uu7&+31#*(k(gken17qywbzf7%cz6cwvgaflhbf
ENV CELERY_BROKER_URL = 'redis://localhost:6379'
ENV CELERY_RESULT_BACKEND = 'redis://localhost:6379'

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]