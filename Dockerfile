FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt .

# psycopg2 requires PostgreSQL headers; tests use SQLite so we skip it.
# Pin pip to avoid resolver noise with very old packages.
RUN pip install --upgrade "pip<24" && \
    grep -v psycopg2 requirements.txt > /tmp/req.txt && \
    pip install -r /tmp/req.txt && \
    pip install coverage

COPY . .

ENV DJANGO_SETTINGS_MODULE=settings.test_settings
ENV SECRET_KEY=test

CMD coverage run --source=url_shortener,shorty \
        --omit='*tests*,*migrations*,*admin*,*wsgi*' \
        manage.py test && \
    coverage report -m
