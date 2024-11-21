
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaccion
from categoria.models import Categoria, SubCategoria
from .forms import TransaccionForm  # Asegúrate de tener un formulario para la transacción
from datetime import timedelta
from django.utils import timezone


@login_required
def listar_gastos_view(request): 
    # Obtener solo los gastos del usuario actual
    gastos = Transaccion.objects.filter(usuario=request.user).select_related('categoria', 'subcategoria')

    # Pasar los datos al contexto
    context = {
        'transacciones': gastos,
    }

    return render(request, 'listar_gastos.html', context)

@login_required
def transacciones_view(request):
    # Si el formulario se envía (POST), procesar el formulario
    if request.method == 'POST':
        transaccion_form = TransaccionForm(request.POST)
        if transaccion_form.is_valid():
            # Crear la transacción pero aún no guardarla
            nueva_transaccion = transaccion_form.save(commit=False)
            # Asignar el usuario actual a la transacción
            nueva_transaccion.usuario = request.user
            # Guardar la transacción con el usuario asignado
            nueva_transaccion.save()
            return redirect('transacciones')  # Redirigir a la vista de transacciones

    else:
        # Si es un GET, inicializar el formulario vacío
        transaccion_form = TransaccionForm()

    # Obtener todas las transacciones del usuario actual
    transacciones = Transaccion.objects.filter(usuario=request.user)

    # Calcular el balance total del usuario
    balance = Transaccion.calcular_balance(request.user)

    # Pasar los datos al contexto
    context = {
        'transaccion_form': transaccion_form,
        'transacciones': transacciones,
        'balance': balance,
    }

    return render(request, 'transacciones.html', context)

@login_required
def historial(request):
    transacciones = Transaccion.objects.filter(usuario=request.user)
    balance = Transaccion.calcular_balance(request.user)
    return render(request, 'history.html', {'transacciones': transacciones, 'balance': balance})

@login_required
def gastos(request):
    """
    Vista para crear una nueva transacción (gasto o ingreso).
    """
    if request.method == 'POST':
        form = TransaccionForm(request.POST, user=request.user)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user  # Asocia la transacción con el usuario actual
            transaccion.save()
            return redirect('gastos')  # Redirige a la lista de transacciones o a una página de confirmación
    else:
        form = TransaccionForm(user=request.user)

    context = {
        'title': 'Crear Transacción',
        'form': form,
    }
    return render(request, 'gastos.html', context)

# Vista para editar una transacción
@login_required
def editar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('listar_gastos')  # Redirigir a la lista de gastos o donde prefieras
    else:
        form = TransaccionForm(instance=transaccion, user=request.user)
    
    return render(request, 'editar.html', {'form': form, 'transaccion': transaccion})

# Vista para ver detalles de una transacción
@login_required
def ver_detalles_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    return render(request, 'detalles_transaccion.html', {'transaccion': transaccion})


@login_required
def eliminar_gasto_view(request, gasto_id):
    # Obtener la transacción o devolver un 404 si no existe
    gasto = get_object_or_404(Transaccion, id=gasto_id, usuario=request.user)

    # Si es una petición POST, eliminamos el gasto
    if request.method == 'POST':
        gasto.delete()
        return redirect('listar_gastos')  # Redirigir a la lista de gastos después de eliminar

    # Si es GET, mostramos una confirmación antes de eliminar
    context = {
        'gasto': gasto,
    }
    return render(request, 'confirmar_eliminar_gasto.html', context)
