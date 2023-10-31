from django.urls import path
from . import views
from .views import Home, CreateEditTemplate, Gallery

app_name = "chat"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("prompt/", CreateEditTemplate.as_view(), name="prompt"),
    path("prompt/<int:id>/", CreateEditTemplate.as_view(), name="prompt-edit"),
    path("fetch_data/<int:id>", views.get_prompt_data, name="fetch_data"),
    path("fetch_data/", views.get_prompt_data, name="fetch_data"),
    path("switch_prompt/<int:id>", views.switch_prompt, name="switch_prompt"),
    path("switch_prompt/", views.switch_prompt, name="switch_prompt"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("gallery", Gallery.as_view(), name="gallery"),
    path("delete_image/<int:id>", views.delete_image, name="delete_image"),
]
