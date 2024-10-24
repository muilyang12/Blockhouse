from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO


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


def generate_predict_pdf_report():
    pass
