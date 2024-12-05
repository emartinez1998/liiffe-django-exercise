from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Empleado
from .serializers import EmpleadoSerializer
from rest_framework.permissions import IsAuthenticated

class EmpleadoList(APIView):   
    def get(self, request):
        permission_classes = [IsAuthenticated]
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)
