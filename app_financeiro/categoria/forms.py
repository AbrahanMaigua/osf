# forms.py
from django import forms
from django.urls import reverse_lazy

from .models import Categoria, SubCategoria

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear una nueva categoría.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', "tipo"]
        success_url = reverse_lazy('categorias')  # Asegúrate de que el nombre coincida con el nombre en urls.py

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input',  # Clase CSS para Bulma
                'placeholder': 'Nombre de la categoría'
            }),
            'tipo': forms.Select(attrs={
                'class': 'input',  # Clase CSS para Bulma
            }),
        }
  
class SubCategoriaForm(forms.ModelForm):
    """
    Formulario para crear una nueva subcategoría asociada a una categoría.
    """
    class Meta:
        model = SubCategoria
        fields = ['nombre', 'categoria']
        success_url = reverse_lazy('categorias')  # Asegúrate de que el nombre coincida con el nombre en urls.py

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input',  # Clase CSS para Bulma
                'placeholder': 'Nombre de la subcategoría'
            }),
            'categoria': forms.Select(attrs={
                'class': 'input'  # Clase CSS para Bulma
            }),
        }

    def __init__(self, *args, **kwargs):
        # Recoger el usuario que se pasa desde la vista
        user = kwargs.pop('user', None)
        super(SubCategoriaForm, self).__init__(*args, **kwargs)

        if user is not None:
            # Filtrar las categorías solo por el usuario autenticado
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)