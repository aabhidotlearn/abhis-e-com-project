# Abhi's e-com

A Django e-commerce demo with product categories, customer signup and login, a session-based cart, checkout, and order history.

## Stack

- Python 3.14
- Django 6.0.5
- SQLite
- Django templates, HTML, and Bootstrap 5

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/>. Use `/admin/` to add categories and products. Product images are stored in `media/`.

Checkout records an order with payment on delivery; no payment provider is configured.

## Configuration

`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` can be set through environment variables. The built-in fallback key is for local development only. Set a private key and turn debug off before deploying.
