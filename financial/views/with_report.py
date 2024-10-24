import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..services import backtest_service, generate_backtest_pdf_report


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
        return HttpResponse(status=400)

    try:
        investment_amount = float(investment_amount)
        buy_ma_period = int(buy_ma_period)
        sell_ma_period = int(sell_ma_period)

    except ValueError:
        print("Invalid parameter types.")

        return HttpResponse(status=400)

    if investment_amount <= 0 or buy_ma_period <= 0 or sell_ma_period <= 0:
        print("Negative values.")

        return HttpResponse(status=400)

    try:
        performance_result = backtest_service(
            symbol, investment_amount, buy_ma_period, sell_ma_period
        )
        final_Result = generate_backtest_pdf_report(symbol, performance_result)

    except ValueError:
        return HttpResponse(status=400)

    return final_Result
