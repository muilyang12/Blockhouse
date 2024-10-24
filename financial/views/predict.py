import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Stock, StockPrice
from ..services import predict_future_price


@csrf_exempt
def predict(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    body = json.loads(request.body)
    symbol = body.get("symbol")

    if not symbol:
        print("No symbol")

        return HttpResponse(status=400)

    try:
        stock = Stock.objects.get(symbol=symbol)
        price = StockPrice.objects.filter(stock=stock).first()
        if price:
            most_recent_timestamp = price.timestamp
        else:
            raise ValueError()

    except Stock.DoesNotExist or ValueError:
        return JsonResponse({"error": "Stock symbol does not exist."})

    prediction_result = predict_future_price(symbol, most_recent_timestamp)

    return JsonResponse(prediction_result, status=200)
