FROM python:3.6-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade "pip<24" && python -m venv /venv

COPY requirements.txt .
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.6-slim

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system app \
    && adduser --system --ingroup app --no-create-home app

WORKDIR /app

COPY --from=builder /venv /venv
COPY . .

ENV PATH="/venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=settings.heroku

# collectstatic needs a non-empty SECRET_KEY to import settings; use a
# build-time placeholder — it is never used at runtime.
RUN SECRET_KEY=build-time-placeholder python manage.py collectstatic --noinput \
    && chmod +x docker-entrypoint.sh \
    && chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "shorty.wsgi", "--bind", "0.0.0.0:8000", "--log-file", "-"]
