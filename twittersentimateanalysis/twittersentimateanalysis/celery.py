import os

import django
from django.apps import apps 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twittersentimateanalysis.settings')

django.setup()

from celery import Celery

from tweetsreplyanalysis import tasks



# Set the default Django settings module for the 'celery' program.


## Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('twittersentimateanalysis')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
# app.tasks.register(tasks.tweetanalysis)

app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'



app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tweetanalysis',
        'schedule': 30.0,
    },
}