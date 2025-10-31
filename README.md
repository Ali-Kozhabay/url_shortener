# URL Shortener

A production-ready URL shortener built with Django, featuring analytics, rate limiting, caching, and async task processing.

## Architecture

- **Django** - Web framework
- **PostgreSQL** - Database
- **Redis** - Caching & message broker
- **Celery** - Async task queue
- **Django REST Framework** - API
- **Nginx** - Reverse proxy & load balancer

## Apps

- `shortener/` - URL shortening & redirect
- `analytics/` - Click tracking & reporting
- `accounts/` - User authentication & plans

## Features

- ✅ URL shortening with random or custom codes
- ✅ Click analytics (device, browser, OS, location)
- ✅ Redis caching for fast redirects
- ✅ Rate limiting (Django + Nginx)
- ✅ Async click tracking with Celery
- ✅ User authentication & authorization
- ✅ REST API with DRF
- ✅ Docker & Docker Compose setup
- ✅ Nginx reverse proxy

## Setup

### Local Development (with Docker)

1. **Clone and setup environment**
   ```bash
   cd /Users/macbook/djngo
   cp .env.example .env
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
   - API: http://localhost/api/
   - Admin: http://localhost/admin/
   - Redirect: http://localhost/{short_code}

### Local Development (without Docker)

1. **Setup virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL and Redis**
   - Install PostgreSQL and create database: `createdb urlshortener`
   - Install and start Redis: `redis-server`

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Create user plans**
   ```bash
   python manage.py shell
   >>> from accounts.models import Plan
   >>> Plan.objects.create(name='free', max_urls=10, max_clicks_per_month=1000, price=0)
   >>> Plan.objects.create(name='basic', max_urls=100, max_clicks_per_month=10000, custom_alias=True, price=9.99)
   >>> Plan.objects.create(name='premium', max_urls=1000, max_clicks_per_month=100000, custom_alias=True, api_access=True, analytics_retention_days=365, price=29.99)
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Start Celery worker (in another terminal)**
   ```bash
   source venv/bin/activate
   celery -A urlshortener worker --loglevel=info
   ```

## API Endpoints

### Shortener

- `POST /api/urls/` - Create short URL
  ```json
  {
    "original_url": "https://example.com",
    "custom_code": "optional",
    "expires_at": "2024-12-31T23:59:59Z"
  }
  ```

- `GET /api/urls/` - List user's URLs
- `GET /api/urls/{id}/` - Get URL details
- `POST /api/urls/{id}/deactivate/` - Deactivate URL
- `GET /{short_code}/` - Redirect to original URL

### Analytics

- `GET /api/analytics/dashboard/` - User dashboard
- `GET /api/analytics/url/{short_code}/?days=30` - URL statistics
- `GET /api/analytics/` - List all clicks

## Rate Limits

- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **URL creation**: 10 per minute per IP (Django + Nginx)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Django 5.0 |
| API | Django REST Framework |
| Database | PostgreSQL 16 |
| Cache/Queue | Redis 7 |
| Task Queue | Celery 5.3 |
| Web Server | Gunicorn |
| Reverse Proxy | Nginx |
| Containerization | Docker & Docker Compose |

## Project Structure

```
djngo/
├── accounts/           # User auth & plans
├── analytics/          # Click tracking & stats
├── shortener/          # URL shortening
├── urlshortener/       # Django project settings
├── docker-compose.yml  # Docker services
├── Dockerfile          # App container
├── nginx.conf          # Nginx config
├── requirements.txt    # Python dependencies
└── README.md
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS` with your domain
3. Set strong `SECRET_KEY`
4. Use production-grade PostgreSQL and Redis
5. Configure SSL/TLS with Let's Encrypt
6. Set up monitoring (e.g., Sentry, Prometheus)
7. Configure backups for PostgreSQL

## License

MIT
