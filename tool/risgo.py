import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Función para calcular el VaR
def calculate_var(ticker, start_date, end_date, confidence_level=0.95):
    # Obtener datos históricos
    data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()

    # Cálculo de VaR
    var = np.percentile(returns, (1 - confidence_level) * 100)

    # Escenarios
    worst_case = returns.min()
    best_case = returns.max()
    mean_case = returns.mean()

    # Calcular la probabilidad de que ocurra cada caso
    worst_case_prob = (returns <= worst_case).mean()
    best_case_prob = (returns >= best_case).mean()
    mean_case_prob = ((returns >= mean_case - 0.01) & (returns <= mean_case + 0.01)).mean()  # rango alrededor del promedio

    return var, worst_case, best_case, mean_case, worst_case_prob, best_case_prob, mean_case_prob


# Función para calcular riesgo
def calculate_risk(ticker, market_ticker, start_date, end_date):
    # Obtener datos históricos
    data = yf.download([ticker, market_ticker], start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()
    
    # Calcular desviación estándar
    std_dev = returns[ticker].std()
    
    # Calcular beta
    covariance = np.cov(returns[ticker], returns[market_ticker])[0][1]
    market_variance = returns[market_ticker].var()
    beta = covariance / market_variance
    
    return std_dev, beta


# Parámetros
ticker = 'MSFT'  # Acción a analizar
market_ticker = '^GSPC'  # Índice del mercado (S&P 500)
start_date = '2020-01-01'
end_date = '2024-01-01'
confidence_level = 0.60

# Calcular riesgo
std_dev, beta = calculate_risk(ticker, market_ticker, start_date, end_date)

# Calcular VaR
var, worst_case, best_case, mean_case, worst_case_prob, best_case_prob, mean_case_prob = calculate_var(
    ticker, start_date, end_date, confidence_level)

# Resultados
print(f"Desviación Estándar de {ticker}: {std_dev:.4f}")
print(f"Beta de {ticker}: {beta:.4f}")
print(f"Valor en Riesgo (VaR) al {confidence_level*100:.1f}%: {var:.4f} ({var*100:.2f}%)")
print(f"Peor caso: {worst_case:.4f} ({worst_case*100:.2f}%)")
print(f"Mejor caso: {best_case:.4f} ({best_case*100:.2f}%)")
print(f"Escenario medio: {mean_case:.4f} ({mean_case*100:.2f}%)")
print(f"Probabilidad de peor caso: {worst_case_prob:.2%}")
print(f"Probabilidad de mejor caso: {best_case_prob:.2%}")
print(f"Probabilidad de escenario medio: {mean_case_prob:.2%}")
