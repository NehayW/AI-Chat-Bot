from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# from django.conf.urls import
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("ai_companion.urls")),
    path("", include("accounts.urls")),
    path("api/", include("accounts.api_urls")),
    path("whatsapp/", include("whatsappbot.urls")), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
