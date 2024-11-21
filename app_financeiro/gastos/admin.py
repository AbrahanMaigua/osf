from django.contrib import admin

from .models import Transaccion, MetaFinanciera

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'subcategoria', 'cantidad', 'fecha', 'tipo')
    search_fields = ('usuario__username', 'categoria__nombre', 'subcategoria__nombre')
    list_filter = ('tipo', 'fecha', 'categoria')

@admin.register(MetaFinanciera)
class MetaFinancieraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'cantidad_objetivo', 'cantidad_acumulada', 'fecha_meta')
    search_fields = ('usuario__username', 'nombre')
    list_filter = ('fecha_meta',)
