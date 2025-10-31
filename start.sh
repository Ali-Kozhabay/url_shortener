#!/bin/bash

echo "🚀 Starting URL Shortener Setup..."

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Run migrations
echo "🗄️  Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Initialize plans
echo "💰 Initializing pricing plans..."
python manage.py init_plans

# Create superuser (optional)
echo "👤 Create a superuser account:"
python manage.py createsuperuser

echo "✅ Setup complete!"
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "To start Celery worker (in another terminal):"
echo "  source venv/bin/activate"
echo "  celery -A urlshortener worker --loglevel=info"
echo ""
echo "To use Docker instead:"
echo "  docker-compose up -d"
echo "  docker-compose exec web python manage.py migrate"
echo "  docker-compose exec web python manage.py init_plans"
echo "  docker-compose exec web python manage.py createsuperuser"
