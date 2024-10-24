import pandas as pd
import pickle


def predict_future_price(symbol, most_recent_timestamp):
    date_range = pd.date_range(start=most_recent_timestamp, periods=30, freq="B")
    date_range_numeric = date_range.astype(int) / 10**9
    date_range_numeric = pd.DataFrame(date_range_numeric, columns=["timestamp_numeric"])

    with open(f"stock_model_{symbol}.pkl", "rb") as f:
        loaded_model = pickle.load(f)

        predicted_prices = loaded_model.predict(date_range_numeric)

    result = {}
    for date, price in zip(date_range.values, predicted_prices):
        result[str(date)] = price

    return result
