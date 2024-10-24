import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle


def build_ml_model(symbol, data):
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["timestamp_numeric"] = data["timestamp"].astype(int) / 10**9

    X = data[["timestamp_numeric"]]
    y = data["close"]

    model = LinearRegression()
    model.fit(X, y)

    with open(f"stock_model_{symbol}.pkl", "wb") as f:
        pickle.dump(model, f)
