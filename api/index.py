import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')

# Use WSGI instead of ASGI
from django.core.wsgi import get_wsgi_application

# Create WSGI application
wsgi_app = get_wsgi_application()

# Convert WSGI to ASGI for Vercel (if needed)
from asgiref.wsgi import WsgiToAsgi

# Export the handler
handler = WsgiToAsgi(wsgi_app)
app = handler