from django.urls import path
from .views import *
from gastos.models import Transaccion

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('transacciones/', transaccion_list, name='transaccion-list'),  # Llama a la función de la vista
    path('subcategorias/<int:categoria_id>/', obtener_subcategorias, name='api-subcategorias'),  # Llama a la función de la vista
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]