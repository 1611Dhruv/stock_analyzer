import logging
import os
import re
from datetime import datetime, timedelta
from typing import List, NamedTuple

import requests

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    raise ValueError("Missing ALPHA_VANTAGE_API_KEY")
URL = "https://www.alphavantage.co/query"

logger = logging.getLogger("financial_data")


class ApiStock(NamedTuple):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


two_years_ago = datetime.now() - timedelta(days=365 * 2)


class ApiError(Exception):
    pass


def fetch_stocks(symbol: str, since: datetime = two_years_ago) -> List[ApiStock]:
    """
    This function fetches from the AlphaVantage for
    stocks for a specific symbol and gets their
    daily stock prices since the since parameter
    which by default is 2 years from now

    Args:
        symbol (str): The symbol of the stock
        since (datetime): The start time through which we are getting the stocks
                          The default is 2 years ago from now

    Returns:
        List[ApiStock]: The list of just the stock prices
    """

    logger.info("fetch_stocks called with param: ", symbol)
    function = "TIME_SERIES_DAILY"
    output_size = "full"

    try:
        url = (
            f"{URL}?function={function}&symbol={symbol}"
            + f"&outputsize={output_size}&apikey={API_KEY}"
        )
        print(url)
        # 10 second timeout
        timeout = 10
        logger.info("Requesting ", url)
        res = requests.get(url, timeout=timeout)

        # Raise if not OK status
        res.raise_for_status()
        # Parse the request as json
        data = res.json()
    except requests.exceptions.Timeout:
        logger.exception("Request Timed Out")
        raise ApiError("Request Timed Out")
    except requests.exceptions.JSONDecodeError:
        logger.exception("Request was not JSON")
        raise ApiError("Request was not JSON")
    except requests.exceptions.HTTPError:
        logger.exception("Request was not an OK status code")
        raise ApiError("Request was not an OK status code")
    except requests.exceptions.RequestException:
        logger.critical("Unknown Request Exception")
        raise ApiError("Unknown Request Exception")

    time_series = "Time Series (Daily)"

    if time_series not in data:
        logger.error("The JSON object doesn't contain ", time_series, " element")
        raise ApiError("No Data")

    open = "1. open"
    high = "2. high"
    low = "3. low"
    close = "4. close"
    volume = "5. volume"

    stocks: List[ApiStock] = []

    # Iterate over all the dates
    for i in data[time_series]:
        if not re.match(r"\d{4}-\d{2}-\d{2}", i):
            logger.error(
                "The JSON doesn't contain the appropriate format.\n",
                " Please Update financial_data/api.py",
            )
            return []

        # If the current date is before the since date
        # we skip it
        if i < since.strftime("%Y-%m-%d"):
            continue
        elm = data[time_series][i]
        if (
            open not in elm
            or high not in elm
            or low not in elm
            or close not in elm
            or volume not in elm
        ):
            logger.error(
                "The JSON doesn't contain the appropriate format.\n",
                " Please Update financial_data/api.py",
            )
            return []
        stocks.append(
            ApiStock(
                datetime.strptime(i, "%Y-%m-%d"),
                float(elm[open]),
                float(elm[high]),
                float(elm[low]),
                float(elm[close]),
                float(elm[volume]),
            )
        )

    return stocks
