
from django.contrib import admin
from django.urls import path, include
from experiencias.views import CreateCheckoutSessionView
from experiencias.views import CreateCoupon

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('api/', include('servicios.urls')),     
    path('api/', include('chatbot.urls')),   
    path('experiencias/create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('experiencias/create-cupon/', CreateCoupon.as_view(), name='create-cupon'),
    path('admin/', admin.site.urls),
    path('', include('empleados.urls')),
    path('', include('experiencias.urls')),
]
