from django.db import models


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    timestamp = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stock", "timestamp"], name="unique_stock_timestamp"
            )
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.stock.symbol} - {self.close_price}"
