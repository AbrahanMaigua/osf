from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MetaAhorro(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Nombre de la meta
    objetivo_monto = models.DecimalField(max_digits=10, decimal_places=2)  # Monto objetivo de ahorro
    monto_ahorrado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Monto ahorrado hasta la fecha
    fecha_inicio = models.DateField(auto_now_add=True)  # Fecha de inicio de la meta
    fecha_limite = models.DateField(null=True, blank=True)  # Fecha límite para alcanzar la meta
    descripcion = models.TextField(blank=True)  # Descripción opcional de la meta

    def porcentaje_completado(self):
        if self.objetivo_monto > 0:
            return (self.monto_ahorrado / self.objetivo_monto) * 100
        return 0

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"

