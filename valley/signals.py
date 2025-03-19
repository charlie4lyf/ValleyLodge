from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os
User = get_user_model()

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'auth':  # Use your app name if using a custom user model
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print("Superuser created successfully!")
        else:
            print("Superuser already exists!")