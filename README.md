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

Docker requires no file copying — just set the env vars (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`).

<img src="http://i.imgur.com/rDkOd8e.png" alt="URL Shortener Screenshot" />
