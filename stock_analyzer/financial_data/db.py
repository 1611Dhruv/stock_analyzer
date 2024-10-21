import logging
from typing import List

import financial_data.models as models
from financial_data.api import ApiStock

logger = logging.getLogger("financial_data")


def save_stock_data(symbol: str, data: List[ApiStock]):
    """
    Helper utility to save the stock data
    """

    logger.info("save_stock_data called with param: ", symbol, "[", data[0], "...")
    db_symbol = models.Symbol.objects.get_or_create(symbol=symbol)

    logger.info("db_symbol: ", db_symbol)
    models.FinancialData.objects.bulk_create(
        [
            models.FinancialData(
                symbol=db_symbol[0],
                date=stock.date,
                open_price=stock.open,
                close_price=stock.close,
                high_price=stock.high,
                low_price=stock.low,
                volume=stock.volume,
            )
            for stock in data
        ],
        update_conflicts=True,
        unique_fields=["symbol", "date"],
        update_fields=[
            "open_price",
            "close_price",
            "high_price",
            "low_price",
            "volume",
        ],
    )
    logger.info("save_stock_data done")
