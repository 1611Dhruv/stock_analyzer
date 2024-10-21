from typing import Dict, List

from financial_data.api import ApiError, ApiStock, fetch_stocks
from financial_data.db import save_stock_data
from financial_data.models import FinancialData, Symbol


def periodic_update():
    """
    Periodically re fetch all the symbols
    """
    symbols = Symbol.objects.all()

    # Just iterate over all symbols and update
    for i in symbols:
        try:
            data = fetch_stocks(i.symbol)
        except ApiError:
            continue
        save_stock_data(i.symbol, data)


def add_symbol(symbol: str):
    """
    The task to add a new symbol
    """
    data = fetch_stocks(symbol)
    save_stock_data(symbol, data)


def get_symbols() -> List[str]:
    """
    Returns a list of symbols
    """
    symbols_str = [db_symbol.symbol for db_symbol in Symbol.objects.all()]
    return symbols_str


def get_data(symbol: str) -> List[Dict]:
    """
    Returns a list of financial data associated with a symbol
    """
    data = FinancialData.objects.all().filter(symbol__symbol=symbol)
    return [
        {
            "date": i.date.strftime("%Y-%m-%d"),
            "open_price": i.open_price,
            "high_price": i.high_price,
            "low_price": i.low_price,
            "close_price": i.close_price,
            "volume": i.volume,
        }
        for i in data
    ]
