from django.utils import timezone
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TransaccionSerializer, SubcategoriaSerializer
from dateutil.relativedelta import relativedelta
from categoria.models import SubCategoria
from gastos.models import Transaccion

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Asegúrate de que el usuario esté autenticado
def obtener_subcategorias(request, categoria_id):
    subcategorias = SubCategoria.objects.filter(categoria_id=categoria_id)  # Filtrar por la categoría seleccionada
    
    # Serializar las subcategorías
    serializer = SubcategoriaSerializer(subcategorias, many=True)
    
    data = {
        'subcategorias': serializer.data  # Asegúrate de que la clave sea 'subcategorias'
    }
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Asegúrate de que el usuario esté autenticado
def transaccion_list(request):
    # Obtener la fecha actual
    fecha_actual = timezone.now()
    
    # Calcular la fecha de hace seis meses
    hace_seis_meses = fecha_actual - relativedelta(months=6)

    # Filtrar las transacciones del usuario actual en los últimos seis meses
    transacciones = Transaccion.objects.filter(
        usuario=request.user,
        fecha__gte=hace_seis_meses,
        fecha__lte=fecha_actual
    )

    # Serializar las transacciones
    serializer = TransaccionSerializer(transacciones, many=True)

    # Calcular el total de gastos por categoría
    total_por_categoria = (
        transacciones
        .filter(tipo='gasto')
        .values('categoria__nombre')
        .annotate(total=Sum('cantidad'))
        .order_by('-total')
    )

    return Response({
        'transacciones': serializer.data,
        'total_por_categoria': total_por_categoria
    })


