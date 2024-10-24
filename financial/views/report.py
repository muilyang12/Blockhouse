import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Stock, StockPrice
from ..services import (
    backtest_service,
    generate_backtest_pdf_report,
    predict_future_price,
    generate_predict_pdf_report,
)


@csrf_exempt
def backtest_with_report(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    body = json.loads(request.body)
    symbol = body.get("symbol")
    investment_amount = body.get("investmentAmount")
    buy_ma_period = body.get("buyMovingAverage")
    sell_ma_period = body.get("sellMovingAverage")

    if not all([symbol, investment_amount, buy_ma_period, sell_ma_period]):
        return JsonResponse(
            {"error": "Not all required parameters arrived."}, status=400
        )

    try:
        investment_amount = float(investment_amount)
        buy_ma_period = int(buy_ma_period)
        sell_ma_period = int(sell_ma_period)

    except ValueError:
        return JsonResponse({"error": "Invalid parameter types."}, status=400)

    if investment_amount <= 0 or buy_ma_period <= 0 or sell_ma_period <= 0:
        return JsonResponse(
            {"error": "Parameters must be positive numbers."}, status=400
        )

    try:
        performance_result = backtest_service(
            symbol, investment_amount, buy_ma_period, sell_ma_period
        )
        final_Result = generate_backtest_pdf_report(symbol, performance_result)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return final_Result


@csrf_exempt
def predict_with_report(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    body = json.loads(request.body)
    symbol = body.get("symbol")

    if not symbol:
        return JsonResponse(
            {"error": "Not all required parameters arrived."}, status=400
        )

    try:
        stock = Stock.objects.get(symbol=symbol)
        price = StockPrice.objects.filter(stock=stock).first()
        if price:
            most_recent_timestamp = price.timestamp
        else:
            raise ValueError()

    except Stock.DoesNotExist or ValueError:
        return JsonResponse({"error": "Not registered stock."})

    prediction_result = predict_future_price(symbol, most_recent_timestamp)

    price_data = StockPrice.objects.filter(stock=stock).values(
        "timestamp", "close_price"
    )
    original_data = [(data["timestamp"], data["close_price"]) for data in price_data]

    final_result = generate_predict_pdf_report(symbol, original_data, prediction_result)

    return final_result
