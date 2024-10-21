import os
import pickle
import tempfile
from datetime import datetime, timedelta

import matplotlib
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ai_integration.models import Predictions
from financial_data.models import Symbol

matplotlib.use("Agg")


class SymbolDNE(Exception):
    """
    Exception to raise when symbol does not exist
    """

    pass


def get_predictions(symbol: str) -> pd.DataFrame:
    """
    We use the pre-trained model to predict stock prices for the next 30 days
    For now our model is simply a linear regression over only one companies
    stock prices. We can add more features and pass the symbol feature in that
    Right now the symbol argument is not used. Can raise SymbolDNE

    Args:
        symbol (str): The symbol of the stock

    Returns:
        pd.DataFrame: The predictions for the next 30 days
    """
    with open("ai_integration/ai_model.pkl", "rb") as file:
        model = pickle.load(file)

    # Find the last date used in the training set (this is assumed, you may need to adjust this if known)
    # We'll assume today as the base date, but this can be adjusted.
    base_date = datetime.today()  # Set the base date manually if known

    # Step 3: Generate predictions for the next 30 days
    next_30_days = [
        (base_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 31)
    ]
    days_since_start = np.arange(1, 31).reshape(-1, 1)

    # Step 4: Predict stock prices for the next 30 days
    # Can add extra features here
    predicted_prices = model.predict(days_since_start)

    # Step 5: Output the predictions
    predictions_df = pd.DataFrame(
        {"date": next_30_days, "predicted_close_price": predicted_prices}
    )

    return predictions_df


def predict_and_save(symbol: str) -> pd.DataFrame:
    """
    This method predicts and saves
    """
    pred_df = get_predictions(symbol)
    save_predictions(symbol, pred_df)
    pred_df.set_index("date", inplace=True)
    return pred_df


def generate_pdf_predictions(df: pd.DataFrame) -> str:
    """
    This returns a pdf endpoint which can be used
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        with PdfPages(tmp.name) as pdf:
            tmp_path = tmp.name

            plt.figure(figsize=(12, 6))

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

            plt.plot(
                df.index,
                df["predicted_close_price"],
                label="Predicted Close Price",
                color="red",
            )

            plt.gcf().autofmt_xdate()

            plt.title("Predicted Stock Price For Next 30 Days")
            plt.xlabel("Date (YYYY-MM-DD)")
            plt.ylabel("Predicted Value")
            plt.legend()
            plt.grid()
            pdf.savefig()
            plt.close()

        return tmp_path


def save_predictions(symbol: str, predictions_df: pd.DataFrame):
    """
    Save the predictions to a CSV file

    Args:
        symbol (str): The symbol of the stock
        predictions_df (pd.DataFrame): The predictions for the next 30 days
    """
    symbol_db = Symbol.objects.all().filter(symbol=symbol)

    if len(symbol_db) != 1:
        print("Failed to find symbol")
        raise SymbolDNE("Failed to find symbol")

    Predictions.objects.bulk_create(
        [
            Predictions(
                symbol=symbol_db[0],
                date=stock[1],
                prediction=stock[2],
            )
            for stock in predictions_df.itertuples()
        ],
        update_conflicts=True,
        unique_fields=["symbol", "date"],
        update_fields=["prediction"],
    )
