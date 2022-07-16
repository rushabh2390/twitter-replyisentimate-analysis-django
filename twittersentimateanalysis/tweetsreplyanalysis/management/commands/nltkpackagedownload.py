from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
import nltk


class Command(BaseCommand):

    def handle(self, *args, **options):
        # The magic line
        list_resource =["twitter_samples","punkt","wordnet","averaged_perceptron_tagger","stopwords","omw-1.4"]
        for resource in list_resource:
            try:
                nltk.data.find(resource)
            except LookupError:
                nltk.download(resource)