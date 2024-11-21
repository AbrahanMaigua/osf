from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gastos.models import Transaccion
from categoria.models import Categoria
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal  # Importar Decimal para manejar cálculos con precisión
from django.db import models

@login_required
def emergencia(request):
    return render(request, 'fondo-emergencia.html')

@login_required
def calcular_presupuesto_categorias(request):
    categorias_presupuesto = []
    fecha_actual = timezone.now()
    # Calcular el primer día del mes actual
    primer_dia_mes = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  
    # Calcular el último día del mes actual
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    
    ingreso_total = Decimal(Transaccion.total_ingresos(request.user))  # Convertir a Decimal
    ingreso_disponible = Decimal(ingreso_total - Transaccion.total_gastos(request.user)  ) 

    categorias = Categoria.objects.filter(usuario=request.user)
    print(categorias)
    if request.method == 'POST':
        # Actualizar el presupuesto mensual de cada categoría y calcular el ingreso disponible
        for categoria in categorias:
            presupuesto = Decimal(request.POST.get(f'presupuesto_{categoria.id}', categoria.presupuesto_mensual))
            categoria.presupuesto_mensual = presupuesto
            categoria.save()

            # Calcular gastos de los últimos 30 días para esta categoría
            gastos = Transaccion.objects.filter(
                categoria=categoria, 
                tipo='gasto',
                fecha__gte=primer_dia_mes,
                fecha__lte=ultimo_dia_mes  # Filtra hasta el último día del mes
                )

    # Preparar datos para la plantilla
    categorias_presupuesto = []
    for categoria in categorias:
        gasto = Transaccion.objects.filter(
            usuario=request.user,
            categoria=categoria,
            tipo='gasto',
            fecha__gte=primer_dia_mes,
            fecha__lte=ultimo_dia_mes  # Filtra hasta el último día del mes
            ).aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0

        print(gasto)
        categorias_presupuesto.append(
            {
                'categoria': categoria,
                'total_gastos':  Decimal(gasto) ,
                'presupuesto_restante':categoria.presupuesto_mensual - gasto,
           
            }
        )

   
    context = {
        'categorias_presupuesto': categorias_presupuesto,
        'ingreso_total': ingreso_total,
        'ingreso_disponible': ingreso_disponible,
    }

    return render(request, 'presupuesto.html', context)
