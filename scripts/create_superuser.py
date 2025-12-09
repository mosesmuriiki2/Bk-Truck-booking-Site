import os
import sys
from pathlib import Path
# Ensure project root is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')
import django

django.setup()

from django.contrib.auth import get_user_model

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ChangeMe123!')

User = get_user_model()
user = User.objects.filter(username=username).first()
if user:
    print('Superuser already exists:', username)
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created:', username)