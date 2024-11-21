<<<<<<< HEAD
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RegistroDeActividades, Setting  # Importa el modelo de auditoría
from django.utils import timezone



def registrar_actividad(user, actividad):
    """Registra una actividad en el modelo de RegistroDeActividades."""
    RegistroDeActividades.objects.create(
        user=user,
        actividad=actividad,
        fecha=timezone.now()
    )


@login_required
def profile(request):
    try:
        setting = Setting.objects.get(usuario=request.user)  # Obtener la configuración del usuario actual
    except Setting.DoesNotExist:
        setting = Setting(usuario=request.user)  # Crear un nuevo objeto Setting si no existe

    if request.method == 'POST':
        form = SettingForm(request.POST, instance=setting)  # Usar un formulario para manejar los ajustes
        if form.is_valid():
            form.save()  # Guardar la configuración
            return redirect('success_page')  # Redirigir a una página de éxito después de guardar
    else:
        form = SettingForm(instance=setting)  # Crear un formulario prellenado con los datos existentes

    registrar_actividad(request.user, "Accedió a la vista de perfil")
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Registrar actividad de registro de usuario
            registrar_actividad(user, "Registro de nuevo usuario")

            messages.success(request, 'Registro exitoso. Inicia sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Sigin.html', {'form': form, 'title':'Registro de usuario'})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Registrar actividad de inicio de sesión
            registrar_actividad(user, "Inicio de sesión exitoso")

            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home')  # Redirigir a una página de inicio o dashboard
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            registrar_actividad(None, f"Intento fallido de inicio de sesión para el usuario {username}")
    
    context = {'title': 'Iniciar Sesión'}
    return render(request, 'login.html', context)
=======
from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request, 'profile.html')
def login(request):
    return render(request, 'login.html')
def sigin(request):
    return render(request, 'sigin.html')
>>>>>>> 89e3e9720cb51446d3bbd46facb6e2aa4915fe0e
