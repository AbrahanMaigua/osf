<<<<<<< HEAD
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Categoria, SubCategoria
from gastos.models import Transaccion
from django.db.models import Sum
from .forms import CategoriaForm, SubCategoriaForm

from django.utils import timezone
from datetime import timedelta

@login_required
def categorias(request):
    if request.method == 'POST':
        if 'categoria_submit' in request.POST:
            # Procesar el formulario de categoría
            categoria_form = CategoriaForm(request.POST)
            if categoria_form.is_valid():
                categoria = categoria_form.save(commit=False)
                categoria.usuario = request.user  # Asignar el usuario actual
                categoria.save()  # Guardar la nueva categoría
                return redirect('categorias')

        elif 'subcategoria_submit' in request.POST:
            # Procesar el formulario de subcategoría, pasando el usuario autenticado
            subcategoria_form = SubCategoriaForm(request.POST, user=request.user)  # Pasar el usuario
            if subcategoria_form.is_valid():
                subcategoria = subcategoria_form.save(commit=False)
                subcategoria.usuario = request.user  # Asignar el usuario actual a la subcategoría
                subcategoria.save()
                return redirect('categorias')

    else:
        # Inicializar los formularios
        categoria_form = CategoriaForm()
        subcategoria_form = SubCategoriaForm(user=request.user)  # Pasar el usuario autenticado

    # Obtener las categorías y subcategorías del usuario autenticado
    categorias = Categoria.objects.filter(usuario=request.user).prefetch_related('subcategorias')


    context = {
        'categoria_form': categoria_form,
        'subcategoria_form': subcategoria_form,
        'title': 'Categorias',
        'categorias': categorias,
    }
    return render(request, 'categorias.html', context)


@login_required
def crear_categoria(request):
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST)
        subcategoria_form = SubCategoriaForm(request.POST)

        if categoria_form.is_valid() and subcategoria_form.is_valid():
            categoria = categoria_form.save()
            subcategoria = subcategoria_form.save(commit=False)
            subcategoria.categoria = categoria  # Asocia la subcategoría a la categoría
            subcategoria.save()
            return redirect('some_success_url')  # Redirige tras el guardado exitoso
    else:
        categoria_form = CategoriaForm()
        subcategoria_form = SubCategoriaForm()

    context = {
        'categoria_form': categoria_form,
        'subcategoria_form': subcategoria_form,
    }
    return render(request, 'crear_categoria.html', context)

@login_required
def crear_subcategoria(request):
    if request.method == 'POST':
        form = SubCategoriaForm(request.POST)
        if form.is_valid():
            subcategoria = form.save(commit=False)
            subcategoria.usuario = request.user  # Asociar la subcategoría con el usuario actual
            subcategoria.save()
            return redirect('subcategorias')  # Redirigir a la lista de subcategorías
    else:
        form = SubCategoriaForm()

    context = {
        'title': 'Crear Subcategoría',
        'form': form,
    }
    return render(request, 'crear_subcategoria.html', context)


@login_required
def detail(request, categoria_id: int, fechas=0):
    # Obtener la fecha actual
    fecha_actual   = timezone.now()
    # Calcular el primer día del mes actual
    primer_dia_mes = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  
    # Calcular el último día del mes actual
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    
    # Obtener la categoría específica
    categoria = get_object_or_404(Categoria, id=categoria_id)
    presupuesto   = categoria.presupuesto_mensual
    gasto   = 0

    subcategoria  = SubCategoria.objects.filter(categoria=categoria)
    transacciones = {}

    for sub in subcategoria:
        # Obtener el total de la cantidad de transacciones para cada subcategoría
        total_cantidad = Transaccion.objects.filter(
            usuario=request.user,
            fecha__gte=primer_dia_mes,
            fecha__lte=ultimo_dia_mes,
            subcategoria=sub).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        gasto += total_cantidad 

        # Sumar al total de la categoría en el diccionario
        if sub.categoria in transacciones:
            transacciones[sub.nombre] += total_cantidad
        else:
            transacciones[sub.nombre] = total_cantidad

    print(transacciones)
    total_gastado = presupuesto - gasto

    context = {
        'title':        categoria.nombre,
        "fecha__gte":   primer_dia_mes,
        "fecha__lte":   ultimo_dia_mes, 
        'presupuesto':  presupuesto,
        'gasto':        gasto,
        'total_gasto':  total_gastado,
        'categoria':    categoria,
        'Transaccion':  transacciones,
        'subcategoria': subcategoria,
    }
    
    return render(request, 'detail.html', context)

@login_required
def subcategoria(request, subcategoria_id: int):
    # Obtener la subcategoría específica
    subcategoria = get_object_or_404(SubCategoria, id=subcategoria_id)
    # Obtener la categoría principal de la subcategoría
    categoria = subcategoria.categoria
    
    # Calcular el total de gastos asociados a esta subcategoría
    total_gastos_subcategoria = Transaccion.objects.filter(
        subcategoria=subcategoria, tipo='gasto'
    ).aggregate(total=Sum('cantidad'))['total'] or 0

    context = {
        'title': subcategoria.nombre,
        'categoria': categoria,
        'subcategoria': subcategoria,
        'total_gastos_subcategoria': total_gastos_subcategoria
    }
    
    return render(request, 'subcategoria.html', context)
=======
from django.shortcuts import render

# Create your views here.
def categorias(request):
   return render(request, 'categorias.html', context={'title':'Categorias'})

def detail(request, categoria_id:int):
   return render(request, 'detail.html', context={'title':'Categorias'})

def subcategoria(request, categoria_id:int):
   return render(request, 'detail.html', context={'title':'Categorias'})
>>>>>>> 89e3e9720cb51446d3bbd46facb6e2aa4915fe0e
