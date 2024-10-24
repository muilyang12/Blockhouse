from django.urls import path
from .views import add_stock, backtest, predict, backtest_with_report

urlpatterns = [
    path("add-stock/", add_stock, name="add_stock"),
    path("backtest/", backtest, name="backtest"),
    path("predict/", predict, name="predict"),
    path("backtest-with-report/", backtest_with_report, name="backtest_with_report"),
]
