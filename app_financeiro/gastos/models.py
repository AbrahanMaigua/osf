# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from categoria.models import Categoria, SubCategoria
from django.conf import settings

from django.utils import timezone
from datetime import timedelta

# Modelo para las Transacciones (Gastos e Ingresos)
class Transaccion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)  # Categoría del gasto
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True, blank=True)  # Subcategoría opcional del gasto
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de la transacción
    tipo = models.CharField(max_length=10, choices=[('gasto', 'Gasto'), ('ingreso', 'Ingreso')])
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo.title()}: {self.cantidad} en {self.categoria} el {self.fecha}"

    class Meta:
        ordering = ['-fecha']

    @staticmethod
    def total_ingresos(usuario):
        """Calcula el total de ingresos del usuario en el mes actual."""
        # Obtener la fecha actual
        # Obtener la fecha actual
        fecha_actual = timezone.now()
        # Calcular el primer día del mes actual
        primer_dia_mes = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
      
        # Calcular el último día del mes actual
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # Obtener el total de ingresos del usuario en el mes actual
        ingresos = Transaccion.objects.filter(
            usuario=usuario,
            tipo='ingreso', 
            fecha__gte=primer_dia_mes,
            fecha__lte=ultimo_dia_mes
        ).aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0
        return ingresos

    @staticmethod
    def total_gastos(usuario):
        """Calcula el total de gastos del usuario en el mes actual."""
          # Obtener la fecha actual
        fecha_actual = timezone.now()
        # Calcular el primer día del mes actual
        primer_dia_mes = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
      
        # Calcular el último día del mes actual
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # Obtener el total de gastos del usuario en el mes actual
        gastos = Transaccion.objects.filter(
            usuario=usuario,
            tipo='gasto',
            fecha__gte=primer_dia_mes,
            fecha__lte=ultimo_dia_mes
        ).aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0
        return gastos

    @staticmethod
    def calcular_balance(usuario):
        """Calcula el balance total del usuario considerando todos los ingresos y gastos."""
        # Total de ingresos y gastos del usuario en general
        ingresos = Transaccion.objects.filter(
            usuario=usuario, tipo='ingreso'
        ).aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0

        gastos = Transaccion.objects.filter(
            usuario=usuario, tipo='gasto'
        ).aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0

        # Calcular el balance total
        return ingresos - gastos


# Modelo para las metas financieras
class MetaFinanciera(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cantidad_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_acumulada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_meta = models.DateField()
    
    def __str__(self):
        return f"Meta: {self.nombre} - Objetivo: {self.cantidad_objetivo}"

