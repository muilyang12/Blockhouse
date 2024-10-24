import os
import requests
from io import StringIO
from requests.exceptions import RequestException, Timeout
from django.db import transaction
from django.http import HttpResponse, JsonResponse

import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from dotenv import load_dotenv

from ..models import Stock, StockPrice

load_dotenv()


def get_save_stock_data(symbol):
    API_KEY = os.getenv("API_KEY")

    if not API_KEY:
        print("API Key is missing. Please check your .env file.")

        raise Exception("Error occured.")

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
    except RequestException or Timeout:
        raise Exception("Failed to get stock data")

    try:
        data = pd.read_csv(StringIO(response.text))
        top_rows = data.head(732)
    except pd.errors.ParserError:
        raise Exception("Wrong data format.")

    try:
        stock = Stock.objects.create(symbol=symbol)

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
        return Exception("Error occured.")

    return top_rows


def build_ml_model(symbol, data):
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["timestamp_numeric"] = data["timestamp"].astype(int) / 10**9

    X = data[["timestamp_numeric"]]
    y = data["close"]

    model = LinearRegression()
    model.fit(X, y)

    with open(f"stock_model_{symbol}.pkl", "wb") as f:
        pickle.dump(model, f)
