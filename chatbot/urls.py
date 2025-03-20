from django.urls import path
from .views import chatbotGet, chatbotPost  # Importa las funciones de vista

urlpatterns = [
    path('chatbot/get/', chatbotGet, name='chatbot-get'),  # Endpoint GET
    path('chatbot/post/', chatbotPost, name='chatbot-post'),  # Endpoint POST
]

