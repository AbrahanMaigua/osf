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
    path('',categorias,  name='categorias'),
<<<<<<< HEAD
    path('<int:categoria_id>/',detail,  name='categorias_detail'),
    path('subcategoria/<int:subcategoria_id>/',subcategoria,  name='subcategorias_detail'),
    path('crear_categoria/', crear_categoria, name='crear_categoria'),
    path('crear_subcategoria/', crear_subcategoria, name='crear_subcategoria'),
    # Otras rutas...

=======
    path('/<int:categoria_id>',detail,  name='categorias'),
    path('subcategoria/<int:sub_id>/',subcategoria,  name='categorias'),
    
    
#
>>>>>>> 89e3e9720cb51446d3bbd46facb6e2aa4915fe0e
]
