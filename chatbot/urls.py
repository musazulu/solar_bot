from django.urls import path
from .views import chat, whatsapp_webhook

urlpatterns = [
    path('chat/', chat),
    path('whatsapp/', whatsapp_webhook),  # ✅ THIS MUST EXIST
]