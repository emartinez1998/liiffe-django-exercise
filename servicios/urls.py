from django.urls import path
from .views import obtener_lugares

urlpatterns = [
    path('tripadvisor/lugares/', obtener_lugares, name='obtener_lugares'),
]
