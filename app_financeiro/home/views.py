from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gastos.models import Transaccion
from metas.models  import MetaAhorro


from django.utils import timezone
from datetime import timedelta


@login_required
def home(request):
    # Obtener la fecha actual
    fecha_actual = timezone.now()
    # Calcular el primer día del mes actual
    primer_dia_mes = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  
    # Calcular el último día del mes actual
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    
    # Mostrar la fecha límite para depuración
    print(f"Fecha inicio del mes: {primer_dia_mes}")
    print(f"Fecha final del mes: {ultimo_dia_mes}")
    print(f"Fecha actual: {fecha_actual}")

    # Obtener solo los gastos del usuario actual en el mes actual
    gastos = Transaccion.objects.filter(
        usuario=request.user,
        fecha__gte=primer_dia_mes,
        fecha__lte=ultimo_dia_mes  # Filtra hasta el último día del mes
    )
    metas = MetaAhorro.objects.filter(usuario=request.user)


    # Calcular el total de los gastos
    #number_gastos = gastos.count()
    total_gastos = Transaccion.total_gastos(request.user)
    total_ingresos = Transaccion.total_ingresos(request.user)

    # Mostrar los gastos para depuración
    print(gastos)

    # Pasar los datos al contexto
    context = {
        'transacciones': gastos,
        'metas': metas,
        'total_gastos': total_gastos,
        'total_ingresos': total_ingresos,
        #'number_gastos': number_gastos,
    }

    return render(request, 'home.html', context)



def politica_privacidad(request):
    return render(request, 'politica_privacidad.html')

