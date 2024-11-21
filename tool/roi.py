import yfinance as yf

def calcular_roi_comparado(ticker, aporte_mensual):
    # Obtener datos históricos de los últimos 12 meses
    accion = yf.Ticker(ticker)
    datos = accion.history(period="1y")
    days = len(datos['Close']) // 12  # Índice para tomar un valor representativo de cada mes

    # Variables para el método de compra fraccionada
    acciones_compradas_frac = 0
    inversion_total_frac = 0
    detalles_compra_frac = []

    # Variables para el método de compra exacta
    acciones_compradas_exacta = 0
    sobrante = 0
    inversion_total_exacta = 0
    detalles_compra_exacta = []

    # Procesamiento mensual
    for i in range(12):
        precio_mes = datos['Close'].iloc[i * days]
        
        # Compra fraccionada
        acciones_mes_frac = aporte_mensual / precio_mes
        acciones_compradas_frac += acciones_mes_frac
        inversion_total_frac += aporte_mensual
        detalles_compra_frac.append((f"Mes {i+1}", precio_mes, acciones_mes_frac))

        # Compra exacta
        if sobrante + aporte_mensual >= precio_mes:
            acciones_mes_exacta = 1
            sobrante = sobrante + aporte_mensual - precio_mes
            detalles_compra_exacta.append((f"Mes {i+1}", precio_mes, acciones_mes_exacta))
            acciones_compradas_exacta += acciones_mes_exacta
        else:
            detalles_compra_exacta.append((f"Mes {i+1}", precio_mes, 0))
            sobrante += aporte_mensual

        inversion_total_exacta += aporte_mensual

    # Precio de la acción al final del periodo
    precio_final = datos['Close'].iloc[-1]

    # Calcular el valor final y ROI para compra fraccionada
    valor_final_frac = acciones_compradas_frac * precio_final
    roi_frac = (valor_final_frac - inversion_total_frac) / inversion_total_frac * 100

    # Calcular el valor final y ROI para compra exacta
    valor_final_exacta = acciones_compradas_exacta * precio_final + sobrante
    roi_exacta = (valor_final_exacta - inversion_total_exacta) / inversion_total_exacta * 100

    # Resultados
    return {
        "Compra Fraccionada": {
            "Total Acciones": acciones_compradas_frac,
            "Inversión Total": inversion_total_frac,
            "Valor Final": valor_final_frac,
            "ROI (%)": roi_frac,
            "Detalle Compra Mensual": detalles_compra_frac
        },
        "Compra Exacta": {
            "Total Acciones": acciones_compradas_exacta,
            "Inversión Total": inversion_total_exacta,
            "Valor Final": valor_final_exacta,
            "Sobrante Final": sobrante,
            "ROI (%)": roi_exacta,
            "Detalle Compra Mensual": detalles_compra_exacta
        }
    }

# Ejemplo de uso
ticker = 'KO'  # Cambia esto al ticker de la acción que desees
aporte_mensual = 166  # Aporte mensual en dólares

resultado = calcular_roi_comparado(ticker, aporte_mensual)

print("Resultados de la inversión comparada:")
for metodo, valores in resultado.items():
    print(f"\nMétodo: {metodo}")
    print(f"Total de Acciones Compradas: {valores['Total Acciones']:.2f}")
    print(f"Inversión Total: ${valores['Inversión Total']:.2f}")
    print(f"Valor Final de la Inversión: ${valores['Valor Final']:.2f}")
    print(f"Retorno sobre la Inversión (ROI): {valores['ROI (%)']:.2f}%")
    if metodo == "Compra Exacta":
        print(f"Sobrante Final no Invertido: ${valores['Sobrante Final']:.2f}")
    print("Detalle Compra Mensual:")
    for mes, precio, acciones in valores['Detalle Compra Mensual']:
        print(f"{mes}: Precio de compra = ${precio:.2f}, Acciones compradas = {acciones:.4f}")
