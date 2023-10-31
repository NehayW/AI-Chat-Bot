from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# from . import views
from .api.api import RegisterView, LoginAPIView, LogoutAPIView, ChatbotResponse


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register-api"),
    path("login/", LoginAPIView.as_view(), name="login-api"),
    path("logout/", LogoutAPIView.as_view(), name="logout-api"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("chat/", ChatbotResponse.as_view(), name="chat"),
]
