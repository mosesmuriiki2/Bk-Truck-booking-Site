import os
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')

# Import Django and get ASGI application
import django
django.setup()

from django.core.asgi import get_asgi_application
from django.core.handlers.asgi import ASGIHandler

# Create the ASGI application
asgi_app = get_asgi_application()

# Vercel expects a handler variable
handler = asgi_app