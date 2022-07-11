from django.urls import path

from .views import dashboard, summary


urlpatterns = [
    path("",dashboard, name="index"),
    path("summary",summary, name="summary"),
]