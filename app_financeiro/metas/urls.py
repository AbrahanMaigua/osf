
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',emergencia, name='metas'),
    path('emergencia/',emergencia, name='fondo_emergencia'),
    path('presupestar/',calcular_presupuesto_categorias, name='presupuesto_categorias'),

]


