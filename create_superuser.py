import os
import django
from django.contrib.auth import get_user_model

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

User = get_user_model()

# Get superuser details from environment variables
username = os.getenv("SUPERUSER_USERNAME", "admin")
email = os.getenv("SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("SUPERUSER_PASSWORD", "securepassword")

# Create superuser if it doesn't exist
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
