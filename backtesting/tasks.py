import os
import tempfile
from typing import Dict

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from backtesting.backtest import backtest

matplotlib.use("Agg")


def generate_pdf_backtest(
    symbol: str, initial_amt: float, enter_wl: int, exit_wl: int
) -> str:
    """
    This function generates a temporary PDF file and returns
    the temp pdf's path
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        with PdfPages(tmp.name) as pdf:
            tmp_path = tmp.name
            backtest_result = backtest(symbol, initial_amt, enter_wl, exit_wl)

            df = backtest_result.portfolio_data
            plt.figure(figsize=(12, 6))
            plt.plot(
                df.index, df["portfolio_value"], label="Portfolio Value", color="blue"
            )
            plt.title("Portfolio Value Over Time")
            plt.xlabel("Date")
            plt.ylabel("Portfolio Value")
            plt.legend()
            plt.grid()
            pdf.savefig()  # Save the plot to PDF
            plt.close

            # Create a text summary of the results
            plt.figure(figsize=(8, 6))
            plt.axis("off")  # Turn off axis
            plt.text(
                0.1,
                0.9,
                f"Total Return: {backtest_result.total_return:.2f}%",
                fontsize=14,
            )
            plt.text(
                0.1,
                0.7,
                f"Max Drawdown: {backtest_result.max_drawdown:.2f}%",
                fontsize=14,
            )
            plt.text(
                0.1, 0.5, f"Number of Trades: {backtest_result.trades}", fontsize=14
            )
            plt.title("Backtesting Summary", fontsize=16)
            pdf.savefig()  # Save the summary to PDF
            plt.close()

        # Return the path to the temporary PDF
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
