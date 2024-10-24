import pandas as pd

from ..models import Stock, StockPrice


def get_backtest_result(
    symbol, initial_investment, buy_ma_period: int, sell_ma_period: int
):
    try:
        stock = Stock.objects.get(symbol=symbol)
    except Stock.DoesNotExist or StockPrice.DoesNotExist:
        raise ValueError("Not registered stock")

    prices = StockPrice.objects.filter(stock=stock).order_by("timestamp")

    if not prices.exists():
        raise ValueError("No price data available for the stock.")

    data = pd.DataFrame.from_records(
        prices.values(
            "timestamp", "open_price", "close_price", "high_price", "low_price"
        )
    )
    data["buy_ma"] = data["close_price"].rolling(window=buy_ma_period).mean().shift(1)
    data["sell_ma"] = data["close_price"].rolling(window=sell_ma_period).mean().shift(1)

    cash = initial_investment
    shares = 0

    peak_value = initial_investment
    max_drawdown = 0

    num_trades = 0

    for _, row in data.iterrows():
        open_price = row["open_price"]
        close_price = row["close_price"]
        high_price = row["high_price"]
        low_price = row["low_price"]
        buy_ma = row["buy_ma"]
        sell_ma = row["sell_ma"]

        if pd.isna(buy_ma) or pd.isna(sell_ma):
            continue

        if low_price < buy_ma and cash >= buy_ma:
            shares_to_buy = int(cash / min(float(open_price), buy_ma))

            shares += shares_to_buy
            cash -= shares_to_buy * buy_ma

            num_trades += 1

        elif high_price > sell_ma and shares > 0:
            cash += shares * sell_ma
            shares = 0

            num_trades += 1

        current_portfolio_value = cash + shares * float(close_price)

        peak_value = max(peak_value, current_portfolio_value)

        drawdown = (peak_value - current_portfolio_value) / peak_value
        max_drawdown = max(max_drawdown, drawdown)

    final_portfolio_value = cash + shares * float(data["close_price"].iloc[-1])

    total_return = final_portfolio_value - initial_investment

    return {
        "total_return": total_return,
        "max_drawdown": max_drawdown,
        "num_trades": num_trades,
    }
