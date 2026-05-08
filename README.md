# URL Shortener

[![CI](https://github.com/smtchahal/url-shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/smtchahal/url-shortener/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/smtchahal/url-shortener/branch/master/graph/badge.svg)](https://codecov.io/gh/smtchahal/url-shortener)

A simple Django-based URL shortening web app.

## Local development

```bash
cp .env.example .env
# Edit .env: set SECRET_KEY to a long random string
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Running locally with Docker

**Prerequisites:** Docker with the Compose plugin (`docker compose version`).

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Long random string (Django secret key) |
| `DB_PASSWORD` | Password for the Postgres container |
| `ALLOWED_HOSTS` | Comma-separated hostnames, e.g. `localhost,127.0.0.1` |

The other variables in `.env.example` can be left as-is for local development.

### 2. Start the app

```bash
docker compose up --build
```

The app will be available at <http://localhost:8000>.

Database migrations run automatically on startup — no manual step needed.

### 3. Stop the app

```bash
docker compose down
```

To also remove the database volume:

> [!CAUTION]
> `docker compose down -v` permanently deletes all database data.

---

### Running tests

The `test` build target runs linting (`flake8`), the test suite, and prints a coverage report:

```bash
docker build --target test -t url-shortener-test .
docker run --rm url-shortener-test
```

<img src="http://i.imgur.com/rDkOd8e.png" alt="URL Shortener Screenshot" />
