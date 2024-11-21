import yfinance as yf
import pandas as pd

pd.set_option('display.max_rows', 100)  # Cambia 100 a cualquier número que necesites

def obtener_datos_financieros(ticker):
    """Obtiene datos financieros de una acción desde Yahoo Finance."""
    accion = yf.Ticker(ticker)
    
    # Obtener el balance general
    balance = accion.balance_sheet
    # Obtener el estado de resultados
    ingresos = accion.financials
    # Obtener el flujo de caja
    flujo_caja = accion.cashflow

    return balance, ingresos, flujo_caja

def calcular_metricas(balance, ingresos):
    """Calcula métricas financieras clave."""
    
    # Imprimir los datos para verificar los nombres de las filas
    print("Balance General:\n", balance)
    print("\nEstado de Resultados:\n", ingresos)

    # Ingresos
    ingresos_totales = ingresos.loc['Total Revenue'][0]
    ingresos_anterior = ingresos.loc['Total Revenue'][1]
    crecimiento_ingresos = (ingresos_totales - ingresos_anterior) / ingresos_anterior * 100
    
    # Margen de beneficio
    beneficio_neto = ingresos.loc['Net Income'][0]
    margen_beneficio = (beneficio_neto / ingresos_totales) * 100

    # Deuda a capital
    # Asegúrate de usar el nombre correcto para las filas de 'Total Liabilities' y 'Shareholder Equity'
    deuda_total = balance.loc['Total Assets'][0] - balance.loc['Total Stockholder Equity'][0]  # Calculando la deuda total
    capital_total = balance.loc['Total Stockholder Equity'][0]
    deuda_a_capital = deuda_total / capital_total

    # Rentabilidad sobre el patrimonio (ROE)
    roe = (beneficio_neto / capital_total) * 100

    return {
        'Ingresos Totales': ingresos_totales,
        'Crecimiento de Ingresos (%)': crecimiento_ingresos,
        'Margen de Beneficio (%)': margen_beneficio,
        'Deuda a Capital': deuda_a_capital,
        'ROE (%)': roe
    }

# Ejemplo de uso
ticker = 'ITUB4.SA'  # Ejemplo: Itaú Unibanco en B3
balance, ingresos, flujo_caja = obtener_datos_financieros(ticker)
metricas = calcular_metricas(balance, ingresos)

# Mostrar resultados
for clave, valor in metricas.items():
    print(f"{clave}: {valor:.2f}")
