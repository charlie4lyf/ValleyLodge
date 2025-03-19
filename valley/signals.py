from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'auth':  # Ensure it runs only for the auth app
        SUPERUSER_USERNAME = "admin"
        SUPERUSER_EMAIL = "monzorabrian@gmail.com"
        SUPERUSER_PASSWORD = "admin123"

        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
            print("Superuser created!")
