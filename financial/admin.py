from django.contrib import admin
from .models import Stock, StockPrice


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["symbol"]
    search_fields = ["symbol"]


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = [
        "stock",
        "timestamp",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
        "volume",
    ]
    search_fields = [
        "stock",
        "timestamp",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
        "volume",
    ]
