# Abhi's e-com

A Python full-stack e-commerce portfolio app built with Django, HTML, CSS, Bootstrap, SQLite, and a JavaScript-enhanced catalog backed by JSON API endpoints.

## Stack

- Python 3.14
- Django 6.0.5
- SQLite
- Django templates, HTML5, CSS3, Bootstrap 5, and vanilla JavaScript
- Same-origin JSON API for category and product browsing

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

## API

The read-only JSON API powers catalog search, category filtering, and sorting in the storefront:

- `GET /api/categories/` returns the available categories.
- `GET /api/products/` returns products. Optional query parameters: `q` for name or description search, `category` for a category ID, and `ordering` (`name`, `price_asc`, or `price_desc`).
- `GET /api/products/<id>/` returns one product or a JSON 404 response.

Example: `/api/products/?q=laptop&ordering=price_asc`

Product responses include the product ID, name, description, price, category, image URL, and product-detail URL. The storefront fetches this data with the browser Fetch API and updates the product cards without a full page reload.

## Tests

Run the Django test suite with:

```bash
python manage.py test
```

## Configuration

`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` can be set through environment variables. The built-in fallback key is for local development only. Set a private key and turn debug off before deploying.
