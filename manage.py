#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dj_database_url
import os


BASE_DIR = ""

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

ALLOWED_HOSTS = ["liiffe-django-exercise-production.up.railway.app"]  # Puedes especificar tu dominio luego


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'  # Agrega esto    
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_pruebas.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
