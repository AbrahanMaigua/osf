# serializers.py
from rest_framework import serializers
from gastos.models import Transaccion
from categoria.models import SubCategoria


class SubcategoriaSerializer(serializers.ModelSerializer):
    # Agrega un campo para el nombre de la categoría

    class Meta:
        model = SubCategoria
        fields = ['id', 'nombre']  # Asegúrate de incluir los campos necesarios


class TransaccionSerializer(serializers.ModelSerializer):
    # Agrega un campo para el nombre de la categoría
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Transaccion
        fields = ['id', 'usuario', 'categoria', 'categoria_nombre', 'subcategoria', 'cantidad', 'fecha', 'tipo', 'descripcion']



        