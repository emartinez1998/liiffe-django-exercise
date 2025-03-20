from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def chatbotGet(request):
    data = {"definicion": "Liiffe es una plataforma de viajes que ofrece itinerarios detallados de 3 días diseñados por lugareños para una experiencia auténtica."}
    return Response(data, status=200)  # Se devuelve JSON con código 200 OK


@api_view(['POST'])
def chatbotPost(request):
    dato = request.data.get('dato')  # Obtiene el valor de 'dato' del request
    if not dato:
        return Response({"error": "El parámetro 'dato' es obligatorio."}, status=400)
    
    mensaje = f"El parámetro 'dato' ha sido recibido: {dato}"
    return Response({"mensaje": mensaje}, status=200)