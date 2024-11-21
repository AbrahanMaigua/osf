<<<<<<< HEAD
from django.conf import settings
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre de la categoría
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional de la categoría
    creada_en = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Relación de muchos a uno con el usuario
    presupuesto_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Presupuesto asignado a la categoría
    tipo = models.CharField(max_length=10, choices=[('gasto', 'Gasto'), ('ingreso', 'Ingreso')], default='Gasto')

    def __str__(self):
        return self.nombre  # Devuelve el nombre de la categoría como representación en texto


class SubCategoria(models.Model):
    usuario     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Relación de muchos a uno con el usuario
    nombre      = models.CharField(max_length=255)  # Nombre de la subcategoría
    categoria   = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)  # Relación con la categoría principal
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional de la subcategoría
    creada_en   = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"{self.nombre}"  # Muestra la subcategoría y su categoría asociada
=======
from django.db import models

# Create your models here.
>>>>>>> 89e3e9720cb51446d3bbd46facb6e2aa4915fe0e
