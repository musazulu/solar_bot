from django.contrib import admin
from django.urls import path
from chatbot.views import chat, whatsapp_webhook, create_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', chat),
    path('api/whatsapp/', whatsapp_webhook),
    path('create-admin/', create_admin),  # 🔥 TEMP FIX
]