import os
import sys
from pathlib import Path

# Add project to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')

# Initialize Django
import django
django.setup()

# Use WSGI instead of ASGI (more stable for Vercel)
from django.core.wsgi import get_wsgi_application
from asgiref.wsgi import WsgiToAsgi

# Create WSGI application
wsgi_app = get_wsgi_application()

# Convert WSGI to ASGI for Vercel
asgi_app = WsgiToAsgi(wsgi_app)

# Export the handler (Vercel looks for this)
handler = asgi_app
app = asgi_app  # Also export as app for compatibility