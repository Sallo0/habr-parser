from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django_admin.settings import SUPERUSER_NAME, SUPERUSER_PASSWORD

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username=SUPERUSER_NAME).exists():
            User.objects.create_superuser(SUPERUSER_NAME, '', SUPERUSER_PASSWORD)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
