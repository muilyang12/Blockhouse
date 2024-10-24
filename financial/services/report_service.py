from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import base64
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime


def html_to_pdf(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()

    return None


def generate_backtest_pdf_report(symbol, performance_result):
    context = {
        "symbol": symbol,
        "result": performance_result,
    }

    html_string = render_to_string("backtest_report.html", context)

    pdf = html_to_pdf(html_string)

    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="output.pdf"'

        return response

    else:
        return JsonResponse({"message": "Failed to create report."})


def generate_predict_pdf_report(symbol, original_data, prediction_result):
    graph_base64 = get_matplotlib_graph(symbol, original_data, prediction_result)

    context = {
        "symbol": symbol,
        "graphImage": graph_base64,
        "result": [
            {"timestamp": timestamp, "price": price}
            for timestamp, price in prediction_result.items()
        ],
    }

    html_string = render_to_string("prediction_report.html", context)

    pdf = html_to_pdf(html_string)

    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="output.pdf"'

        return response

    else:
        return JsonResponse({"message": "Failed to create report."})


def get_matplotlib_graph(symbol, original_data, prediction_data):
    matplotlib.use("Agg")

    history_timestamps = []
    history_prices = []
    for timestamp, price in original_data:
        history_timestamps.append(timestamp)
        history_prices.append(price)

    prediction_timestamps = []
    prediction_prices = []
    for timestamp, price in prediction_data.items():
        timestamp_trimmed = timestamp.split(".")[0]
        prediction_timestamps.append(
            datetime.strptime(timestamp_trimmed, "%Y-%m-%dT%H:%M:%S").date()
        )
        prediction_prices.append(float(price))

    plt.scatter(history_timestamps, history_prices, label="Price", color="blue")
    plt.scatter(prediction_timestamps, prediction_prices, label="Price", color="red")

    plt.title(f"Stock Prices for {symbol}")

    plt.xlabel("Timestamp")
    plt.ylabel("Close Price")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    image_base64 = f"data:image/png;base64,{image_base64}"

    plt.close()

    return image_base64
