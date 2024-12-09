from django.urls import path
from .api import ExperienciaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/experiencias', ExperienciaViewSet, 'experiencias')
urlpatterns = router.urls
