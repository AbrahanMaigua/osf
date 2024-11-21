import yfinance as yf
import pandas as pd

def obtener_datos_accion(ticker, start_date, end_date):
    """Obtiene datos históricos de precios de una acción desde Yahoo Finance."""
    accion = yf.download(ticker, start=start_date, end=end_date, interval='1mo')
    return accion['Adj Close']

def simular_inversion(ticker, monto_inicial, aporte_regular, frecuencia, duracion_meses):
    """Simula el crecimiento de una inversión en acciones."""
    # Obtener datos de precios de la acción
    precios = obtener_datos_accion(ticker, '2020-01-01', '2024-01-01')
    
    meses_por_año = 12
    meses_total = duracion_meses
    
    # Inicializar monto total y lista para el crecimiento
    monto_total = monto_inicial
    crecimiento_mensual = []

    # Recorrer los meses y calcular el crecimiento
    for mes in range(meses_total):
        # Obtener el precio de la acción correspondiente al mes actual
        precio_actual = precios.iloc[mes]

        if mes < len(precios):
            acciones_compradas = monto_total // precio_actual
            
            # Actualizar el monto total (comprar acciones)
            monto_total += acciones_compradas * precio_actual
            
            # Añadir el aporte regular si es el mes de aporte
            if mes % (meses_por_año // frecuencia) == 0:  # Aporte regular según la frecuencia
                monto_total += aporte_regular
        
        crecimiento_mensual.append((mes + 1, 
                              round(monto_total, 2),
                              round(precio_actual, 2))
            )

    return crecimiento_mensual


def calcular_ahorro_anual(monto_inicial, aporte_regular, frecuencia, tasa_interes, duracion):
    # Mapeo de frecuencia a su valor anual
    frecuencia_anual = {"diario": 365, "semanal": 52, "mensual": 12, "anual": 1}
    n = frecuencia_anual[frecuencia]
    r = tasa_interes / 100

    # Inicializa el monto total con el monto inicial
    monto_total = monto_inicial
    aux = monto_total
    
    # Lista para almacenar el crecimiento año a año
    crecimiento_anual = []

    # Calcula el crecimiento año a año
    for año in range(1, duracion + 1):
        # Calcula el monto acumulado al final del año actual
        aux = monto_total - aux

        monto_total = monto_total * (1 + r / n) ** n + aporte_regular * (((1 + r / n) ** n - 1) / (r / n))

        # Guarda el monto al final del año en la lista de crecimiento anual
        crecimiento_anual.append((año, 
                            round(monto_total, 2),
                            round(aux, 2)) )
        
    return crecimiento_anual

# Ejemplo de uso


resultado = calcular_ahorro_anual(100, 100, "mensual", 5, 10)

# Muestra el crecimiento año a año
for año, monto, acumulado in resultado:
    print(f"Año {año}: Monto acumulado = R$ {monto}, {acumulado}")

# Ejemplo de uso
ticker    = 'ITUB4.SA'  # Ejemplo: Itaú Unibanco en B3
resultado = simular_inversion(ticker, 100, 100, 1, 24)  # Aporte mensual durante 24 meses

# Mostrar el crecimiento mensual
for mes, monto, aux in resultado:
    print(f"Mes {mes}: Monto acumulado = ${monto} {aux}")
