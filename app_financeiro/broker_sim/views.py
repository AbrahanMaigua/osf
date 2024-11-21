# trading/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Portfolio, Transaction
import yfinance as yf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='1d')['Close'].iloc[-1]

def buy_stock(request):
    if request.method == "POST":
        ticker = request.POST['ticker']
        shares = int(request.POST['shares'])
        portfolio = Portfolio.objects.first()  # Suponiendo que solo hay un usuario para simplificar

        price_per_share = get_stock_price(ticker)
        total_cost = price_per_share * shares

        if total_cost <= portfolio.balance:
            portfolio.balance -= total_cost
            portfolio.save()
            Transaction.objects.create(portfolio=portfolio, ticker=ticker, shares=shares,
                                        price_per_share=price_per_share, transaction_type='buy')
            return redirect('portfolio')
        else:
            return HttpResponse("Insufficient balance to complete the purchase.")

    return render(request, 'buy_stock.html')

def sell_stock(request):
    if request.method == "POST":
        ticker = request.POST['ticker']
        shares = int(request.POST['shares'])
        portfolio = Portfolio.objects.first()  # Suponiendo que solo hay un usuario para simplificar

        transactions = Transaction.objects.filter(portfolio=portfolio, ticker=ticker, transaction_type='buy')
        total_shares = sum(t.shares for t in transactions)

        if total_shares >= shares:
            price_per_share = get_stock_price(ticker)
            portfolio.balance += price_per_share * shares
            portfolio.save()
            Transaction.objects.create(portfolio=portfolio, ticker=ticker, shares=shares,
                                        price_per_share=price_per_share, transaction_type='sell')
            return redirect('portfolio')
        else:
            return HttpResponse("Insufficient shares to sell.")

    return render(request, 'sell_stock.html')

def portfolio_view(request):
    portfolio = Portfolio.objects.first()  # Suponiendo que solo hay un usuario para simplificar
    transactions = Transaction.objects.filter(portfolio=portfolio)

    return render(request, 'portfolio.html', {'portfolio': portfolio, 'transactions': transactions})
