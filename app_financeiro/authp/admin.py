from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personalizada', {
            'fields': (
                'nombre_completo',
                'telefono',
                'fecha_nacimiento',
                'direccion',
                'preferencias_comunicacion',
                'configuracion_privacidad',
                'tema_preferido',
                'intereses',
            ),
        }),
    )

    list_display = (
        'username', 
        'nombre_completo', 
        'telefono', 
        'fecha_nacimiento', 
        'direccion', 
        'tema_preferido', 
        'is_staff',
    )
    search_fields = ('username', 'nombre_completo', 'telefono', 'tema_preferido')
    list_filter = ('is_staff', 'is_superuser', 'tema_preferido', 'configuracion_privacidad')

admin.site.register(CustomUser, CustomUserAdmin)
