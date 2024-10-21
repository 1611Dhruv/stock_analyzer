from collections import namedtuple

import pandas as pd

from financial_data.models import FinancialData

BacktestResult = namedtuple(
    "BacktestResult", ["portfolio_data", "total_return", "max_drawdown", "trades"]
)


class BacktestError(Exception):
    pass


def backtest(
    symbol: str, initial_amt: float, enter_wl: int, exit_wl: int
) -> BacktestResult:
    """
    This function performs the backtesting
    """
    data = load_saved_symbol(symbol)
    return backtest_logic(data, initial_amt, enter_wl, exit_wl)


def load_saved_symbol(symbol: str) -> pd.DataFrame:
    """
    This function loads the saved symbol
    """
    # Retrieve the data into a dataframe
    data = pd.DataFrame(
        FinancialData.objects.all()
        .filter(symbol__symbol=symbol)
        .values("date", "close_price")
    )
    data.set_index("date", inplace=True)
    data.index = pd.to_datetime(data.index)

    # Handle the no data case
    if data.empty:
        raise BacktestError("No data found for symbol")
    return data


def backtest_logic(
    data: pd.DataFrame, initial_amt: float, enter_wl: int, exit_wl: int
) -> BacktestResult:
    """
    This function performs the backtesting logic
    """
    # Compute the moving averages
    data["enter_ma"] = data["close_price"].rolling(window=enter_wl).mean()
    data["exit_ma"] = data["close_price"].rolling(window=exit_wl).mean()

    # Now we shall simulate the scenario
    cash = initial_amt
    shares_owned = 0
    trades = 0

    # Initialize a portfolio column
    data["portfolio_value"] = initial_amt
    for i, row in data.iterrows():
        close_price = row["close_price"]

        if row.isnull().any():
            continue

        # Sell the stocks first
        if close_price > row["exit_ma"] and shares_owned > 0:
            # Sell all stocks
            cash += shares_owned * close_price
            shares_owned = 0
            trades += 1

        if close_price < row["enter_ma"] and cash > close_price:
            # Buy as many as possible
            shares_to_buy = cash // close_price
            shares_owned += shares_to_buy
            cash -= shares_to_buy * close_price
            trades += 1

        data.at[i, "portfolio_value"] = cash + shares_owned * close_price

    total_return = (data["portfolio_value"].iloc[-1] - initial_amt) / initial_amt * 100
    max_drawdown = (
        (data["portfolio_value"].cummax() - data["portfolio_value"])
        / data["portfolio_value"].cummax()
    ).max() * 100

    portfolio_data = data[["portfolio_value"]].reset_index()
    return BacktestResult(portfolio_data, total_return, max_drawdown, trades)
