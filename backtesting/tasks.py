import os
import tempfile
from typing import Dict

from backtesting.backtest import backtest


def generate_pdf_backtest(
    symbol: str, initial_amt: float, enter_wl: int, exit_wl: int
) -> str:
    """
    This function generates a temporary PDF file and returns
    the temp pdf's path
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp_path = tmp.name
        backtest_result = backtest(symbol, initial_amt, enter_wl, exit_wl)

        return tmp_path


def generate_json_backtest(
    symbol: str, initial_amt: float, enter_wl: int, exit_wl: int
) -> Dict:
    """
    This function generates a temporary PDF file and returns
    the temp pdf's path
    """
    backtest_result = backtest(symbol, initial_amt, enter_wl, exit_wl)
    backtest_result.portfolio_data.set_index("date", inplace=True)
    backtest_result.portfolio_data.index = (
        backtest_result.portfolio_data.index.strftime("%Y-%m-%d")
    )

    return_json = {
        "total_return": backtest_result.total_return,
        "max_drawdown": backtest_result.max_drawdown,
        "trades": backtest_result.trades,
        "portfolio_data": backtest_result.portfolio_data.to_dict(),
    }

    return return_json
