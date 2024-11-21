"""
URL configuration for app_financeiro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
<<<<<<< HEAD
    path('',               gastos,     name='gastos'),
    path('historial',      historial,  name='history'),
    #path('metas/',         metas,      name='metas'),
    path('transacciones/', transacciones_view, name='transacciones'),
    path('gastos/',        listar_gastos_view, name='listar_gastos'),
    path('gastos/eliminar/<int:gasto_id>/', eliminar_gasto_view, name='eliminar_gasto'),
    path('editar/<int:transaccion_id>/', editar_transaccion, name='editar_transaccion'),
    path('detalles/<int:transaccion_id>/', ver_detalles_transaccion, name='ver_detalles_transaccion'),
]
=======
    path('',gastos,           name='gastos'),
    path('historial',historial,  name='history'),
    path('metas/',metas,       name='metas'),

#
]
>>>>>>> 89e3e9720cb51446d3bbd46facb6e2aa4915fe0e
