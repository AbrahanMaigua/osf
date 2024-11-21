from django.contrib import admin
from .models import Categoria, SubCategoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'creada_en', 'usuario', 'presupuesto_mensual')
    search_fields = ('nombre', 'usuario__username')
    list_filter = ('creada_en', 'usuario')

class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'descripcion', 'creada_en', 'usuario')
    search_fields = ('nombre', 'categoria__nombre', 'usuario__username')
    list_filter = ('creada_en', 'usuario', 'categoria')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
