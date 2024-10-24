import json
import requests
import pandas as pd
from io import StringIO

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Stock, StockPrice
from ..services import build_ml_model

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

    stock = Stock.objects.create(symbol=symbol)

    API_KEY = "JYTVQCUC2OTBNKYH"

    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",
        "apikey": API_KEY,
        "datatype": "csv",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except (RequestException, Timeout):
        Stock.objects.delete(symbol=symbol)

        return HttpResponse(status=500)

    try:
        data = pd.read_csv(StringIO(response.text))
        top_rows = data.head(732)
    except pd.errors.ParserError:
        Stock.objects.delete(symbol=symbol)

        return HttpResponse(status=500)

    try:
        with transaction.atomic():
            for _, row in top_rows.iterrows():
                StockPrice.objects.create(
                    stock=stock,
                    timestamp=row["timestamp"],
                    open_price=row["open"],
                    close_price=row["close"],
                    high_price=row["high"],
                    low_price=row["low"],
                    volume=row["volume"],
                )
    except:
        Stock.objects.delete(symbol=symbol)

        return HttpResponse(status=500)

    build_ml_model(data)

    return HttpResponse(status=201)
