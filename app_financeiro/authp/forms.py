from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Setting

 
class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['moneda_preferida', 'notificaciones_email', 'tema', 'idioma']  # Campos que deseas incluir en el formulario

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para la creación de un nuevo usuario con campos personalizados y estilos CSS.
    """
    email = forms.CharField(
        max_length=255,
        required=False,
        help_text='email.',
        widget=forms.TextInput(attrs={
            'class': 'input',  # Bulma class for text input
            'placeholder': 'Escribe tu correo electronico'
        })
    )
    nombre_completo = forms.CharField(
        max_length=255,
        required=False,
        help_text='Opcional. Nombre completo del usuario.',
        widget=forms.TextInput(attrs={
            'class': 'input',  # Bulma class for text input
            'placeholder': 'Escribe tu nombre completo'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        help_text='Opcional. Número de teléfono.',
        widget=forms.TextInput(attrs={
            'class': 'input',  # Bulma class for text input
            'placeholder': 'Escribe tu número de teléfono'
        })
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1900, 2100),
            attrs={
                'class': 'select'  # Bulma class for select dropdown
            }
        )
    )
    direccion = forms.CharField(
        max_length=255,
        required=False,
        help_text='Opcional. Dirección del usuario.',
        widget=forms.TextInput(attrs={
            'class': 'input',  # Bulma class for text input
            'placeholder': 'Escribe tu dirección'
        })
    )
    preferencias_comunicacion = forms.ChoiceField(
        choices=[('email', 'Email'), ('sms', 'SMS')],
        required=False,
        help_text='Opcional. Método preferido de comunicación.',
        widget=forms.Select(attrs={
            'class': 'select'  # Bulma class for select dropdown
        })
    )
    configuracion_privacidad = forms.BooleanField(
        initial=False,
        required=True,
        help_text='Aceptar compartir datos.',
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox'  # Bulma class for checkbox
        })
    )
    consentimiento_datos = forms.BooleanField(
        initial=False,
        required=True,
        help_text='Aceptar el amacenamentos de datos.',
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox',  # Bulma class for checkbox


        })
    )

    tema_preferido = forms.ChoiceField(
        choices=[('light', 'Claro'), ('dark', 'Oscuro')],
        required=False,
        help_text='Opcional. Tema preferido.',
        widget=forms.Select(attrs={
            'class': 'select'  # Bulma class for select dropdown
        })
    )
    intereses = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea',  # Bulma class for text area
            'placeholder': 'Escribe tus intereses'
        }),
        required=False,
        help_text='Opcional. Intereses del usuario.'
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'input '}
    ),
    help_text='Opcional. Fecha de nacimiento.'
    )


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email",'username', 'password1', 'password2',
                  'nombre_completo', 'telefono',
                  'fecha_nacimiento', 'direccion',
                  'preferencias_comunicacion',
                  'configuracion_privacidad',
                  'consentimiento_datos',

                   'tema_preferido', 'intereses')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nombre de usuario'}),
            # Los widgets para password se especificarán en el init
        }

        # Añadir clases CSS a los campos de contraseña en __init__
        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
           # Aplicamos clases CSS personalizadas a todos los campos
            self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Nombre de usuario'})
            self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Contraseña'})

            self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirmar contraseña'})
            




    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'nombre_completo', 'telefono', 'fecha_nacimiento', 'direccion', 'preferencias_comunicacion', 'configuracion_privacidad', 'tema_preferido', 'intereses')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # Aplicamos clases CSS personalizadas a todos los campos
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirmar contraseña'})
        
        # Puedes añadir el mismo tratamiento a otros campos si es necesario

