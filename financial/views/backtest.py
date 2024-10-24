import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..services import backtest_service


@csrf_exempt
def backtest(request):
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
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(performance_result, status=200)
