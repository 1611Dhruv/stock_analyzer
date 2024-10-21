from datetime import datetime
from typing import List
from unittest.mock import patch

from django.test import TestCase
from financial_data.api import ApiStock, fetch_stocks
from requests.models import Response

from .db import save_stock_data
from .models import FinancialData, Symbol


class TestFetch(TestCase):
    """
    This class contains the several tests for the fetching of stocks
    """

    @patch("requests.get")
    def test_mock_success(self, mock_get):
        mock_response = Response()
        mock_response.status_code = 200
        # Mocks a sample response
        with open("financial_data/mock.json", "r") as f:
            mock_response._content = f.read().encode()

        mock_get.return_value = mock_response

        expected: List[ApiStock] = [
            ApiStock(
                date=datetime.strptime("2024-10-18", "%Y-%m-%d"),
                open=231.9200,
                high=232.6499,
                low=230.1700,
                close=232.2000,
                volume=4715688,
            ),
            ApiStock(
                date=datetime.strptime("2024-10-17", "%Y-%m-%d"),
                open=232.0000,
                high=233.1450,
                low=230.6550,
                close=232.8800,
                volume=5040092,
            ),
            ApiStock(
                date=datetime.strptime("2024-10-16", "%Y-%m-%d"),
                open=232.1100,
                high=233.8800,
                low=231.1200,
                close=233.6700,
                volume=2846669,
            ),
            ApiStock(
                date=datetime.strptime("2024-10-15", "%Y-%m-%d"),
                open=236.4000,
                high=237.3700,
                low=232.7100,
                close=232.9600,
                volume=3350556,
            ),
        ]

        stocks = fetch_stocks("IBM")

        self.assertEqual(stocks, expected)
        self.assertEqual(mock_get.call_count, 1)


class TestDb(TestCase):

    def test_save_stock_data(self):
        symbol = "IBM"
        data = [
            ApiStock(
                date=datetime.strptime("2024-10-18", "%Y-%m-%d"),
                open=231.9200,
                high=232.6499,
                low=230.1700,
                close=232.2000,
                volume=4715688,
            ),
            ApiStock(
                date=datetime.strptime("2024-10-17", "%Y-%m-%d"),
                open=232.0000,
                high=233.1450,
                low=230.6550,
                close=232.8800,
                volume=5040092,
            ),
            ApiStock(
                date=datetime.strptime("2024-10-16", "%Y-%m-%d"),
                open=232.1100,
                high=233.8800,
                low=231.1200,
                close=233.6700,
                volume=2846669,
            ),
            ApiStock(
                date=datetime.strptime("2024-10-15", "%Y-%m-%d"),
                open=236.4000,
                high=237.3700,
                low=232.7100,
                close=232.9600,
                volume=3350556,
            ),
        ]

        # Assert that initilly count is 0
        self.assertEqual(FinancialData.objects.count(), 0)
        self.assertEqual(Symbol.objects.count(), 0)

        save_stock_data(symbol, data)

        stock = FinancialData.objects.all().filter(symbol__symbol=symbol)

        # Assert the counts
        self.assertEqual(FinancialData.objects.count(), 4)
        self.assertEqual(Symbol.objects.count(), 1)

        # Reverse the data for order and then check
        data.reverse()
        for i in range(len(data)):
            self.assertEqual(
                stock[i].date.strftime("%Y-%m-%d"), data[i].date.strftime("%Y-%m-%d")
            )
            self.assertEqual(stock[i].open_price, data[i].open)
            self.assertEqual(stock[i].close_price, data[i].close)
            self.assertEqual(stock[i].high_price, data[i].high)
            self.assertEqual(stock[i].low_price, data[i].low)
            self.assertEqual(stock[i].volume, data[i].volume)
