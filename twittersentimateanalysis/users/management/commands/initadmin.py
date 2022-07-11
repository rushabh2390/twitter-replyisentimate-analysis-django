from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        print(os.environ.get("DJANGO_SUPERUSER_EMAIL"),os.getenv("DJANGO_SUPERUSER_USERNAME"),os.getenv("DJANGO_SUPERUSER_PASSWORD"))
        # The magic line
        user = User.objects.get(username=os.getenv("DJANGO_SUPERUSER_USERNAME"))
        user.set_password(os.getenv("DJANGO_SUPERUSER_PASSWORD"))
        user.email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        user.save()