from django.urls import path
from . import views
from .views import UserSignup, UserLogin, LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", UserSignup.as_view(), name="sign-up"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
