from django.urls import path
from .views import EmpleadoList
from .api import EmpleadoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/empleados',EmpleadoViewSet, 'empleados')
urlpatterns = router.urls
