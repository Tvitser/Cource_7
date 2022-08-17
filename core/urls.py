from django.urls import path

from core import views
from rest_framework.authtoken import views as rest_views
urlpatterns = [
    path("signup", views.SignupView.as_view()),
    path("login", views.LoginView.as_view()),
    path("profile", views.ProfileView.as_view()),
    path("update_password", views.UpdatePasswordView.as_view()),
    path('token_login', rest_views.obtain_auth_token),
]