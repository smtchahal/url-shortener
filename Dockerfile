FROM python:3.6-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade "pip<24"

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM builder AS test

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=settings.test_settings
ENV SECRET_KEY=test

CMD ["sh", "-c", "flake8 && python manage.py test"]


FROM python:3.6-slim

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system app \
    && adduser --system --ingroup app --no-create-home app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY . .

ENV DJANGO_SETTINGS_MODULE=settings.heroku

RUN rm -f requirements-dev.txt \
    && SECRET_KEY=build-time-placeholder python manage.py collectstatic --noinput \
    && chmod +x docker-entrypoint.sh \
    && chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "shorty.wsgi", "--bind", "0.0.0.0:8000", "--log-file", "-"]
