from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Experiencia
from .serializers import ExperienciaSerializer
from rest_framework.permissions import IsAuthenticated

import stripe
import time
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ExperienciaList(APIView):   
    def get(self, request):        
        experiencias = Experiencia.objects.all()
        serializer = ExperienciaSerializer(experiencias, many=True)
        return Response(serializer.data)
    





# Configurar la API de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener el monto desde los parámetros de la URL (?amount=5000)
            amount = request.GET.get('amount', 5000)  # Monto en centavos (50 USD por defecto)

            # Validar que el monto sea un número
            try:
                amount = int(amount)
                if amount <= 0:
                    raise ValueError("El monto debe ser mayor a 0")
            except ValueError:
                return Response({"error": "El monto debe ser un número positivo"}, status=status.HTTP_400_BAD_REQUEST)

            # Crear la sesión de pago en Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Pago personalizado"
                            },
                            "unit_amount": amount,  # Monto en centavos
                        },
                        "quantity": 1,                    
                    }
                ],
                success_url="https://tu-sitio.com/success",
                cancel_url="https://tu-sitio.com/cancel",
                discounts=[{"coupon": "i7KHG0TB"}], 
            )

            # Retornar la URL de pago
            return Response({"url": session.url}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        



class CreateCoupon(APIView):
    def post(self, request):
        data = request.data  # Datos del formulario

        # Extraer datos con valores por defecto
        percent_off = data.get("percent_off")
        amount_off = data.get("amount_off")
        currency = data.get("currency")
        duration = data.get("duration")
        duration_in_months = data.get("duration_in_months")
        max_redemptions = data.get("max_redemptions")
        redeem_by = data.get("redeem_by")
        coupon_id = data.get("id")

        # 🔹 **Validaciones**
        # 1️⃣ Verificar que `duration` sea válido
        if duration not in ["once", "repeating", "forever"]:
            return Response({"error": "El campo 'duration' debe ser 'once', 'repeating' o 'forever'."}, status=status.HTTP_400_BAD_REQUEST)

        # 2️⃣ Verificar que se haya definido un tipo de descuento
        if not percent_off and not amount_off:
            return Response({"error": "Debes proporcionar 'percent_off' o 'amount_off'."}, status=status.HTTP_400_BAD_REQUEST)

        if percent_off and amount_off:
            return Response({"error": "No puedes usar 'percent_off' y 'amount_off' al mismo tiempo."}, status=status.HTTP_400_BAD_REQUEST)

        # 3️⃣ Si se usa `amount_off`, `currency` es obligatorio
        if amount_off and not currency:
            return Response({"error": "Si usas 'amount_off', 'currency' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # 4️⃣ Si `duration` es "repeating", `duration_in_months` es obligatorio
        if duration == "repeating" and not duration_in_months:
            return Response({"error": "Si 'duration' es 'repeating', 'duration_in_months' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # 5️⃣ Convertir `redeem_by` a timestamp si está presente
        if redeem_by:
            try:
                redeem_by = int(time.mktime(time.strptime(redeem_by, "%Y-%m-%d")))  # Convertir fecha a timestamp
            except ValueError:
                return Response({"error": "Formato de 'redeem_by' inválido. Usa 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 **Construcción del cupón**
        coupon_data = {
            "duration": duration,
            "id": coupon_id if coupon_id else None,  # Usa el ID si está presente
            "max_redemptions": max_redemptions,
            "redeem_by": redeem_by
        }

        if percent_off:
            coupon_data["percent_off"] = percent_off
        else:
            coupon_data["amount_off"] = amount_off
            coupon_data["currency"] = currency

        if duration == "repeating":
            coupon_data["duration_in_months"] = duration_in_months

        # 🔹 **Crear el cupón en Stripe**
        try:
            coupon = stripe.Coupon.create(**{k: v for k, v in coupon_data.items() if v is not None})
            return Response(coupon, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
