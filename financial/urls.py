from django.urls import path
from .views import add_stock

urlpatterns = [path("add-stock/", add_stock, name="add_stock")]
