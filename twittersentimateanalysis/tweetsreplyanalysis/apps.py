import types
from typing import Optional
from django.apps import AppConfig
import nltk
import sys


class TweetsreplyanalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweetsreplyanalysis'

    def __init__(self, app_name: str, app_module: Optional[types.ModuleType]) -> None:
        super().__init__(app_name, app_module)
        list_resource =["twitter_samples","punkt","wordnet","averaged_perceptron_tagger","stopwords","omw-1.4"]
        for resource in list_resource:
            try:
                nltk.data.find(resource)
            except LookupError:
                nltk.download(resource)