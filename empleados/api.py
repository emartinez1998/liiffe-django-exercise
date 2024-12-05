from .models import Empleado
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import EmpleadoSerializer


class EmpleadoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Empleado.objects.all()
    #permission_classes = [permissions.AllowAny] 
    serializer_class = EmpleadoSerializer