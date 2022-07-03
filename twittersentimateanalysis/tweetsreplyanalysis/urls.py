from django.urls import path

from .views import dashboard, summary


urlpatterns = [
    path("index",dashboard, name="index"),
    path("summary",summary, name="summary"),
]