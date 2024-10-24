from django.urls import path
from .views import add_stock, backtest, predict

urlpatterns = [
    path("add-stock/", add_stock, name="add_stock"),
    path("backtest/", backtest, name="backtest"),
    path("predict/", predict, name="predict"),
]
