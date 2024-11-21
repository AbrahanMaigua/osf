import yfinance as yf

class Stock:
    def __init__(self, symbol, sector, quantity):
        self.symbol = symbol
        self.sector = sector
        self.quantity = quantity
        self.price = self.get_current_price()

    def get_current_price(self):
        stock_data = yf.Ticker(self.symbol)
        return stock_data.history(period="1d")['Close'].iloc[-1]

    def total_value(self):
        return self.quantity * self.price

    def invested_value(self):
        """Calcula el valor invertido en esta acción."""
        return self.price * self.quantity

class Portfolio:
    def __init__(self):
        self.stocks = []

    def add_stock(self, stock):
        """Añadir o actualizar la cantidad de acciones en el portafolio."""
        for s in self.stocks:
            if s.symbol == stock.symbol:
                s.quantity += stock.quantity
                return
        self.stocks.append(stock)

    def total_value(self):
        return sum(stock.total_value() for stock in self.stocks)

    def total_invested(self):
        """Calcula el total invertido en el portafolio."""
        return sum(stock.invested_value() for stock in self.stocks)

    def sector_distribution(self):
        sector_values = {}
        for stock in self.stocks:
            sector_values[stock.sector] = sector_values.get(stock.sector, 0) + stock.total_value()
        return sector_values

    def balance_portfolio(self, target_distribution, additional_investment=0):
        sector_values = self.sector_distribution()
        total_value = self.total_value() + additional_investment

        recommendations = {}

        for sector, target_percentage in target_distribution.items():
            target_value = total_value * target_percentage
            current_value = sector_values.get(sector, 0)
            difference = target_value - current_value

            if difference > 0:
                # Sugerir comprar más acciones
                recommendations[sector] = {
                    'action': 'buy',
                    'amount': difference,
                    'stocks': self.recommend_buy(sector, difference),
                    'additional_investment': self.suggest_investment(sector, difference)  # Sugerir dónde invertir
                }
            elif difference < 0:
                # Sugerir vender acciones
                recommendations[sector] = {
                    'action': 'sell',
                    'amount': -difference,
                    'stocks': self.recommend_sell(sector, -difference)
                }
            else:
                recommendations[sector] = {
                    'action': 'balanced',
                    'amount': 0,
                    'stocks': []
                }

        return recommendations

    def recommend_buy(self, sector, amount):
        """ Sugerir qué acciones comprar en un sector específico. """
        stocks_in_sector = [s for s in self.stocks if s.sector == sector]
        suggestions = []
        for stock in stocks_in_sector:
            # Calcular cuántas acciones comprar
            shares_to_buy = amount // stock.price
            if shares_to_buy > 0:
                suggestions.append({
                    'symbol': stock.symbol,
                    'price': stock.price,
                    'shares': shares_to_buy
                })
        return suggestions

    def recommend_sell(self, sector, amount):
        """ Sugerir qué acciones vender en un sector específico. """
        stocks_in_sector = [s for s in self.stocks if s.sector == sector]
        suggestions = []
        for stock in stocks_in_sector:
            # Calcular cuántas acciones a vender
            shares_to_sell = min(stock.quantity, amount // stock.price)
            if shares_to_sell > 0:
                suggestions.append({
                    'symbol': stock.symbol,
                    'price': stock.price,
                    'shares': shares_to_sell
                })
        return suggestions

    def suggest_investment(self, sector, amount):
        """ Sugerir dónde realizar aportes adicionales en un sector específico. """
        stocks_in_sector = [s for s in self.stocks if s.sector == sector]
        suggestions = []
        for stock in stocks_in_sector:
            # Calcular cuántas acciones se pueden comprar con el monto disponible
            shares_to_buy = amount // stock.price
            if shares_to_buy > 0:
                suggestions.append({
                    'symbol': stock.symbol,
                    'price': stock.price,
                    'shares': shares_to_buy
                })
        return suggestions

    def execute_recommendations(self, recommendations, additional_investment=0):
        for sector, recommendation in recommendations.items():
            action = recommendation['action']
            if action == 'buy':
                for stock in recommendation['stocks']:
                    # Añadir acciones al portafolio o actualizar la cantidad
                    self.add_stock(Stock(stock['symbol'], sector, stock['shares']))
                    print(f"Comprando {stock['shares']} acciones de {stock['symbol']} a ${stock['price']:.2f} cada una.")
            elif action == 'sell':
                for stock in recommendation['stocks']:
                    # Vender acciones del portafolio
                    for s in self.stocks:
                        if s.symbol == stock['symbol']:
                            if s.quantity >= stock['shares']:
                                s.quantity -= stock['shares']
                                print(f"Vendiendo {stock['shares']} acciones de {stock['symbol']} a ${stock['price']:.2f} cada una.")
                            break
            
            if additional_investment > 0:
                # Realizar la inversión adicional
                for stock in recommendation.get('additional_investment', []):
                    self.add_stock(Stock(stock['symbol'], sector, stock['shares']))
                    print(f"Realizando una inversión adicional de {stock['shares']} acciones de {stock['symbol']} a ${stock['price']:.2f} cada una.")

    def print_portfolio(self):
        """Muestra un resumen del portafolio con los valores de cada acción."""
        total_value = self.total_value()
        print("\nResumen del Portafolio:")
        print(f"{'Acción':<10} {'Cantidad':<10} {'Precio':<10} {'Valor':<10} {'Porcentaje':<10}")
        for stock in self.stocks:
            stock_value = stock.total_value()
            percentage = (stock_value / total_value) * 100 if total_value > 0 else 0
            print(f"{stock.symbol:<10} {stock.quantity:<10} {stock.price:<10.2f} {stock_value:<10.2f} {percentage:<10.2f}%")
        print(f"{'Total':<10} {'':<10} {'':<10} {total_value:<10.2f} {'100.00%':<10}")

# Ejemplo de uso con acciones de la B3
portfolio = Portfolio()
portfolio.add_stock(Stock("VALE3.SA", "Materiales", 1))  # Vale
portfolio.add_stock(Stock("LREN3.SA", "Consumo Discrecional", 1))  # Lojas Renner
portfolio.add_stock(Stock("PETR3.SA", "Energía", 9))  # Petrobras
portfolio.add_stock(Stock("ELET3.SA", "Energía", 3))  # Eletrobras
portfolio.add_stock(Stock("BBAS3.SA", "Bancos", 3))  # Banco do Brasil
portfolio.add_stock(Stock("BBDC3.SA", "Bancos", 17))  # Bradesco

# Definir la distribución objetivo por sector
target_distribution = {
    "Materiales": 0.2,
    "Consumo Discrecional": 0.2,
    "Energía": 0.3,
    "Bancos": 0.3
}

# Definir un valor adicional a invertir
additional_investment = 0  # Cambia este valor según sea necesario

# Balancear el portafolio
recommendations = portfolio.balance_portfolio(target_distribution, additional_investment)

# Mostrar recomendaciones
for sector, recommendation in recommendations.items():
    action = recommendation['action']
    amount = recommendation['amount']
    stocks = recommendation.get('stocks', [])
    
    if action == 'buy':
        print(f"\n{sector}: Comprar ${amount:.2f} en acciones.")
        for stock in stocks:
            print(f"  Comprar {stock['shares']} acciones de {stock['symbol']} a ${stock['price']:.2f} cada una.")
    elif action == 'sell':
        print(f"\n{sector}: Vender ${amount:.2f} en acciones.")
        for stock in stocks:
            print(f"  Vender {stock['shares']} acciones de {stock['symbol']} a ${stock['price']:.2f} cada una.")
    else:
        print(f"\n{sector}: Balanceado.")

# Ejecutar recomendaciones
portfolio.execute_recommendations(recommendations, additional_investment)

# Mostrar el valor total invertido en el portafolio
total_invested = portfolio.total_invested()
print(f"\nValor total invertido en el portafolio: ${total_invested:.2f}")

# Mostrar el resumen del portafolio
portfolio.print_portfolio()
