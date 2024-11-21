# trading/models.py
from django.db import models

class Portfolio(models.Model):
    user = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)

class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    shares = models.IntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)  # "buy" or "sell"
    timestamp = models.DateTimeField(auto_now_add=True)
