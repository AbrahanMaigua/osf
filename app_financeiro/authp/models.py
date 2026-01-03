from django.contrib.auth.models import AbstractUser
from django.db import models
from cryptography.fernet import Fernet
import base64
from django.conf import settings

# Initialize cipher suite if ENCRYPTION_KEY is available and valid.
# If the key is missing/invalid, fall back to no-encryption mode to allow the app to start.
cipher_suite = None
encryption_key = getattr(settings, 'ENCRYPTION_KEY', None)
if encryption_key:
    try:
        cipher_suite = Fernet(encryption_key.encode())
    except Exception as e:
        print(f"Error al inicializar Fernet: {e}")


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
        # Encrypt sensitive fields if cipher is available, otherwise store plaintext
        if cipher_suite and self.nombre_completo:
            self.nombre_completo = base64.b64encode(cipher_suite.encrypt(self.nombre_completo.encode())).decode()
        if cipher_suite and self.telefono:
            self.telefono = base64.b64encode(cipher_suite.encrypt(self.telefono.encode())).decode()
        if cipher_suite and self.direccion:
            self.direccion = base64.b64encode(cipher_suite.encrypt(self.direccion.encode())).decode()
        super(CustomUser, self).save(*args, **kwargs)

    def get_nombre_completo(self):
        if not self.nombre_completo:
            return None
        if cipher_suite:
            try:
                return cipher_suite.decrypt(base64.b64decode(self.nombre_completo.encode())).decode()
            except Exception:
                return self.nombre_completo
        return self.nombre_completo

    def get_telefono(self):
        if not self.telefono:
            return None
        if cipher_suite:
            try:
                return cipher_suite.decrypt(base64.b64decode(self.telefono.encode())).decode()
            except Exception:
                return self.telefono
        return self.telefono

    def get_direccion(self):
        if not self.direccion:
            return None
        if cipher_suite:
            try:
                return cipher_suite.decrypt(base64.b64decode(self.direccion.encode())).decode()
            except Exception:
                return self.direccion
        return self.direccion

    def delete_user_data(self):
        self.nombre_completo = None
        self.telefono = None
        self.fecha_nacimiento = None
        self.direccion = None
        self.save()


class Setting(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    moneda_preferida = models.CharField(max_length=10, default='USD')
    notificaciones_email = models.BooleanField(default=True)
    tema = models.CharField(max_length=20, choices=[('light', 'Claro'), ('dark', 'Oscuro')], default='light')
    idioma = models.CharField(max_length=10, choices=[('es', 'Español'), ('en', 'Inglés')], default='es')

    def __str__(self):
        return f"Ajustes de {self.usuario.username}"

    def eliminar_datos(self):
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
