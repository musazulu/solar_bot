from django.urls import path
from .views import chat, whatsapp_webhook, create_admin

urlpatterns = [
    path('chat/', chat),
    path('whatsapp/', whatsapp_webhook),
    path('create-admin/', create_admin),
]