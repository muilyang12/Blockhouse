import json
import requests
import pandas as pd
from io import StringIO

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Stock, StockPrice
from ..services import get_save_stock_data, build_ml_model

from django.db import transaction
from requests.exceptions import RequestException, Timeout


@csrf_exempt
def add_stock(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    body = json.loads(request.body)
    symbol = body.get("symbol")

    if not symbol:
        return HttpResponse(status=400)

    if Stock.objects.filter(symbol=symbol).exists():
        return JsonResponse({"error": "Stock symbol already exists."}, status=400)

    try:
        data = get_save_stock_data(symbol)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    build_ml_model(symbol, data)

    return HttpResponse(status=201)
