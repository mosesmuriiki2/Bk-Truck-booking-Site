import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')

# Expose ASGI application for Vercel Python runtime
from django.core.asgi import get_asgi_application
app = get_asgi_application()

# Vercel's @vercel/python will import `application` from this file
# and serve it for each request as a serverless function.