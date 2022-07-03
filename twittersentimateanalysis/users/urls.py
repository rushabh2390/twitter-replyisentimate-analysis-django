from django.urls import path

from .views import login_request, signup_view, logout_request


urlpatterns = [
    path('register', signup_view, name='register'),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
]