import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 1. Obtener datos históricos de acciones
tickers = ['AAPL', 'MSFT']
start_date = '2020-01-01'
end_date = '2024-01-01'

data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
returns = data.pct_change().dropna()

# 2. Definir parámetros para la simulación
initial_investment = 100000  # Inversión inicial
n_simulations = 1000        # Número de simulaciones
n_periods = 252              # Días de negociación en un año

# 3. Calcular rendimientos esperados y volatilidades
mean_returns = returns.mean()  # Rendimiento medio diario
volatilities = returns.std()    # Volatilidad diaria
correlation_matrix = returns.corr()  # Matriz de correlación

# 4. Generar una matriz de Cholesky
cholesky_matrix = np.linalg.cholesky(correlation_matrix)

# 5. Inicializar una matriz para almacenar los resultados
def run_simulation():
    portfolio_values = np.zeros((n_simulations, n_periods))
    portfolio_values[:, 0] = initial_investment

    # 6. Simulación de Monte Carlo
    for t in range(1, n_periods):
        random_normals = np.random.randn(n_simulations, len(tickers))
        correlated_randoms = random_normals @ cholesky_matrix.T
        
        # Ajustar el cálculo de asset_returns
        asset_returns = (mean_returns.values / n_periods + 
                         volatilities.values * correlated_randoms / np.sqrt(n_periods))
        
        # Calcular el valor del portafolio para este período
        portfolio_values[:, t] = portfolio_values[:, t - 1] * (1 + asset_returns).prod(axis=1)
    
    return portfolio_values

# 7. Repetir la simulación varias veces
n_repeats = 5  # Número de veces que quieres repetir la simulación
all_portfolio_values = []

for _ in range(n_repeats):
    print(f"simulacion numero {len(all_portfolio_values)}")
    result = run_simulation()
    all_portfolio_values.append(result)

# 8. Visualización de las simulaciones
plt.figure(figsize=(10, 6))
for portfolio_values in all_portfolio_values:
    plt.plot(portfolio_values.T, color='blue', alpha=0.01)
plt.title("Simulación de Monte Carlo para el Portafolio (AAPL y MSFT)")
plt.xlabel("Días de Negociación")
plt.ylabel("Valor del Portafolio")
plt.grid()

# Guardar la imagen
plt.savefig('simulacion_portafolio_repetida.png', dpi=300)


# 9. Estadísticas de Resultados
final_values = [result[:, -1] for result in all_portfolio_values]
mean_final_values = [np.mean(values) for values in final_values]
median_final_values = [np.median(values) for values in final_values]
var_95 = [np.percentile(values, 5) for values in final_values]  # Valor en Riesgo al 95%

for i in range(n_repeats):
    print(f"Simulación {i + 1}:")
    print(f"Valor final medio del portafolio: ${mean_final_values[i]:.2f}")
    print(f"Valor final mediano del portafolio: ${median_final_values[i]:.2f}")
    print(f"Valor en Riesgo (VaR) al 95%: ${initial_investment - var_95[i]:.2f}")
    print()
