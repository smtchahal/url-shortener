# URL Shortener

[![Build Status](https://travis-ci.org/smtchahal/url-shortener.svg?branch=master)](https://travis-ci.org/smtchahal/url-shortener)
[![Coverage Status](https://coveralls.io/repos/github/smtchahal/url-shortener/badge.svg?branch=master)](https://coveralls.io/github/smtchahal/url-shortener?branch=master)

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
