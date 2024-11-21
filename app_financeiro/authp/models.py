<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser
from django.db import models
from cryptography.fernet import Fernet
import base64
from django.conf import settings
settings.AUTH_USER_MODEL,

# Usa la clave de cifrado almacenada en el archivo .env
cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())

class CustomUser(AbstractUser):
    nombre_completo = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    preferencias_comunicacion = models.CharField(max_length=50, blank=True, null=True)
    tema_preferido = models.CharField(max_length=50, blank=True, null=True)
    intereses = models.TextField(blank=True, null=True)
    configuracion_privacidad = models.BooleanField(default=False)
    
    consentimiento_datos = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Cifrado de datos sensibles antes de guardarlos
        if self.nombre_completo:
            self.nombre_completo = base64.b64encode(cipher_suite.encrypt(self.nombre_completo.encode())).decode()
        if self.telefono:
            self.telefono = base64.b64encode(cipher_suite.encrypt(self.telefono.encode())).decode()
        if self.direccion:
            self.direccion = base64.b64encode(cipher_suite.encrypt(self.direccion.encode())).decode()
        super(CustomUser, self).save(*args, **kwargs)

    def get_nombre_completo(self):
        if self.nombre_completo:
            return cipher_suite.decrypt(base64.b64decode(self.nombre_completo.encode())).decode()
        return None

    def get_telefono(self):
        if self.telefono:
            return cipher_suite.decrypt(base64.b64decode(self.telefono.encode())).decode()
        return None

    def get_direccion(self):
        if self.direccion:
            return cipher_suite.decrypt(base64.b64decode(self.direccion.encode())).decode()
        return None

    def delete_user_data(self):
        self.nombre_completo = None
        self.telefono = None
        self.fecha_nacimiento = None
        self.direccion = None
        self.save()



class Setting(models.Model):
    # Relación uno a uno con el usuario para almacenar sus preferencias personalizadas
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Preferencia de moneda para mostrar precios o costos en la moneda deseada
    moneda_preferida = models.CharField(max_length=10, default='USD')
    
    # Permiso para recibir notificaciones por correo; el usuario puede revocarlo en cualquier momento
    notificaciones_email = models.BooleanField(default=True)
    
    # Preferencia de tema visual, claro u oscuro, para personalizar la apariencia de la aplicación
    tema = models.CharField(max_length=20, choices=[('light', 'Claro'), ('dark', 'Oscuro')], default='light')

    # Idioma preferido de la interfaz de usuario
    idioma = models.CharField(max_length=10, choices=[('es', 'Español'), ('en', 'Inglés')], default='es')
    
    def __str__(self):
        return f"Ajustes de {self.usuario.username}"
    
    def eliminar_datos(self):
        """Método para eliminar o anonimizar datos del usuario de acuerdo con la LGPD."""
        self.moneda_preferida = ''
        self.notificaciones_email = False
        self.tema = ''
        self.idioma = ''
        self.save()


class RegistroDeActividades(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    actividad = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Actividad de {self.user.username} en {self.fecha}"
=======
from django.db import models

# Create your models here.
>>>>>>> 89e3e9720cb51446d3bbd46facb6e2aa4915fe0e
