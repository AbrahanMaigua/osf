# forms.py
from django import forms
from .models import Transaccion 
from categoria.models import Categoria, SubCategoria

class TransaccionForm(forms.ModelForm):
    """
    Formulario para crear una nueva transacción (gasto o ingreso).
    """
    class Meta:
        model = Transaccion
        fields = ['categoria', 'subcategoria', 'cantidad', 'tipo', 'descripcion']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'input ', 'id':'categoria-select'}),
            'subcategoria': forms.Select(attrs={'class': 'input ', 'id':'subcategoria-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Ingrese la cantidad'}),
            'tipo': forms.Select(attrs={'class': 'input'}),
            'descripcion': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Descripción de la transacción'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Recoger el usuario que se pasa desde la vista
        user = kwargs.pop('user', None)
        super(TransaccionForm, self).__init__(*args, **kwargs)
        

        if user:
            # Filtrar las categorías por el usuario autenticado
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
            
            # Filtrar las subcategorías según la categoría seleccionada
            if 'categoria' in self.data:
                try:
                    categoria_id = int(self.data.get('categoria'))
                    self.fields['subcategoria'].queryset = SubCategoria.objects.filter(categoria_id=categoria_id)
                except (ValueError, TypeError):
                    self.fields['subcategoria'].queryset = SubCategoria.objects.none()
            elif self.instance.pk:  # Si es una instancia existente, obtener la categoría seleccionada
                self.fields['subcategoria'].queryset = SubCategoria.objects.filter(categoria=self.instance.categoria)
            else:
                self.fields['subcategoria'].queryset = SubCategoria.objects.none()   
