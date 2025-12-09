import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel's @vercel/python will import `application` from this file
# and serve it for each request as a serverless function.