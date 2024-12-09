from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Experiencia
from .serializers import ExperienciaSerializer
from rest_framework.permissions import IsAuthenticated

class ExperienciaList(APIView):   
    def get(self, request):        
        experiencias = Experiencia.objects.all()
        serializer = ExperienciaSerializer(experiencias, many=True)
        return Response(serializer.data)
