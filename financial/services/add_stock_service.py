import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle


def build_ml_model(data):
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["timestamp_numeric"] = data["timestamp"].astype(int) / 10**9

    X = data[["timestamp_numeric"]]
    y = data["close"]

    model = LinearRegression()
    model.fit(X, y)

    with open("stock_model.pkl", "wb") as f:
        pickle.dump(model, f)
