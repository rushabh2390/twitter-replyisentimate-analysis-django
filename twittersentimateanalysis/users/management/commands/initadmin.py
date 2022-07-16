from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        # The magic line
        if User.objects.count() > 0:
            user = User.objects.get(username=os.getenv("DJANGO_SUPERUSER_USERNAME"))
            if user:
                user.set_password(os.getenv("DJANGO_SUPERUSER_PASSWORD"))
                user.email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
                user.save()
                return
        User.objects.create_superuser(username=os.getenv("DJANGO_SUPERUSER_USERNAME"),
                                 email=os.environ.get("DJANGO_SUPERUSER_EMAIL"),
                                 password=os.getenv("DJANGO_SUPERUSER_PASSWORD"))