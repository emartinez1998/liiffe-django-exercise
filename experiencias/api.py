from .models import Experiencia
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import ExperienciaSerializer


class ExperienciaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Experiencia.objects.all()
    #permission_classes = [permissions.AllowAny] 
    serializer_class = ExperienciaSerializer