from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_admin.django_admin.settings import SUPERUSER_NAME, SUPERUSER_PASSWORD


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username=SUPERUSER_NAME).exists():
        User.objects.create_superuser(SUPERUSER_NAME, '', SUPERUSER_PASSWORD)