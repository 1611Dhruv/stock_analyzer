from unittest.mock import patch

import pandas as pd
from django.test import TestCase
from requests.models import Response

from backtesting.backtest import backtest, backtest_logic
from financial_data.tasks import add_symbol


class TestBackTest(TestCase):

    def test_backtest_logic_no_trade(self):
        """
        This test only tests the logic portion for the backtest
        """

        dummy_amt = 10000.0

        # Create a dummy dataframe
        data = pd.DataFrame()
        data["date"] = pd.date_range("2024-01-01", periods=10)
        data["close_price"] = [1 for _ in range(10)]
        data.set_index("date", inplace=True)

        # Expected portfolio_data
        expected = pd.DataFrame()
        expected["date"] = pd.date_range("2024-01-01", periods=10)
        expected["portfolio_value"] = [dummy_amt for _ in range(10)]
        # Run the backtest
        result = backtest_logic(data, dummy_amt, 5, 5)

        # Check that no trades were made
        self.assertEqual(result.trades, 0)
        self.assertEqual(result.total_return, 0)
        self.assertEqual(result.max_drawdown, 0)
        self.assertTrue(result.portfolio_data.equals(expected))

    def test_backtest_logic_no_drawdown(self):
        """
        Consider scenario where window lengths are: 2(sell) and 3(buy)

        Moving averges of previous day must be used to determine current day
           Buy Sell <-- Buy if price < buy avg and sell if price > sell avg
        10 - -
        10 10 -
        10 10 10 <- Nothing
        15 12.5 35/3 <- Nothing (Sell but no stocks)
        10 12.5 35/3 <- Buy
        20 15 15 <- Sell
        20 20 50/3 <- Nothing (Sell but no stocks)
        20 20 20 <- Nothing (Sell but no stocks)
        10 15 50/3 <- Buy

        Expected portfolio
        10000 10000 0
        10000 10000 0
        10000 10000 0
        10000 10000 0
        10000 10000 0
        20000 20000 0
        20000 20000 0
        20000 20000 0
        20000 20000 0
        """
        initial_amt = 10000
        closing_prices = [10, 10, 10, 15, 10, 20, 20, 20, 10]

        expectedPf = [10000, 10000, 10000, 10000, 10000, 20000, 20000, 20000, 20000]
        days = len(closing_prices)
        expectedTrades = 3
        expectedReturn = (expectedPf[-1] - initial_amt) / initial_amt * 100
        # Drawdown here is 0 because the peak value in each period is the same as portfolio value
        expectedDrawdown = 0

        # Create a dummy dataframe
        df = pd.DataFrame()
        df["date"] = pd.date_range("2024-01-01", periods=days)
        df["close_price"] = closing_prices
        df.set_index("date", inplace=True)

        # Expected portfolio_data
        expected = pd.DataFrame()
        expected["date"] = pd.date_range("2024-01-01", periods=days)
        expected["portfolio_value"] = expectedPf

        # Run the backtest
        result = backtest_logic(df, initial_amt, 2, 3)

        # Check that no trades were made
        self.assertEqual(result.trades, expectedTrades)
        self.assertEqual(result.total_return, expectedReturn)
        self.assertEqual(result.max_drawdown, expectedDrawdown)
        self.assertTrue(result.portfolio_data.equals(expected))

    def test_backtest_logic_with_drawdown(self):
        """
        We will test with drawdown now. Buy win is 2, sell win is 3.
        Prices are as follows:
        initial_amt = $10,000

        10 - - <- N
        10 10 - <- N
        10 10 10 <- N
        5 7.5 8.33 <- Buy 2000 @ 5 left with $0
        0 2.5 5 <- Hold
        15 7.5 6.67 <- Sell 2000 @ 15 left with $30,000
        5 10 6.67 <- Buy 6000 @ 5 left with 0

        Here is the expected PF
        pf max drawdown
        10,000 10k 0%
        10,000 10k 0%
        10,000 10k 0%
        10,000 10k 0%
        0      10k 100%
        30,000 30k 0%
        30,000 30k 0%
        """
        initial_amt = 10000
        closing_prices = [10, 10, 10, 5, 0, 15, 5]

        expectedPf = [10000, 10000, 10000, 10000, 0, 30000, 30000]
        days = len(closing_prices)
        expectedTrades = 3
        expectedReturn = (expectedPf[-1] - initial_amt) / initial_amt * 100
        expectedDrawdown = 100

        # Create a dummy dataframe
        df = pd.DataFrame()
        df["date"] = pd.date_range("2024-01-01", periods=days)
        df["close_price"] = closing_prices
        df.set_index("date", inplace=True)

        # Expected portfolio_data
        expected = pd.DataFrame()
        expected["date"] = pd.date_range("2024-01-01", periods=days)
        expected["portfolio_value"] = expectedPf

        # Run the backtest
        result = backtest_logic(df, initial_amt, 2, 3)

        # Check that no trades were made
        self.assertEqual(result.trades, expectedTrades)
        self.assertEqual(result.total_return, expectedReturn)
        self.assertEqual(result.max_drawdown, expectedDrawdown)
        self.assertTrue(result.portfolio_data.equals(expected))

    @patch("requests.get")
    def test_backtest_end_to_end(self, mock_get):
        """
        This is an end to end test which tests the entire backtest method
        The mock.json data used here is the same test case as test_backtest_logic_no_drawdown
        """
        initial_amt = 10000
        closing_prices = [10, 10, 10, 15, 10, 20, 20, 20, 10]

        expectedPf = [
            10000,
            10000,
            10000,
            10000,
            10000,
            20000,
            20000,
            20000,
            20000,
        ]
        days = len(closing_prices)
        expectedTrades = 3
        expectedReturn = (expectedPf[-1] - initial_amt) / initial_amt * 100
        # Drawdown here is 0 because the peak value in each period is the same as portfolio value
        expectedDrawdown = 0

        # Expected portfolio_data
        expected = pd.DataFrame()
        expected["date"] = pd.date_range("2024-10-10", periods=days)
        expected["portfolio_value"] = expectedPf

        # Mock the IBM request

        mock_resp = Response()
        mock_resp.status_code = 200
        with open("backtesting/mock.json") as f:
            mock_resp._content = f.read().encode("utf8")
        mock_resp.headers["content-type"] = "application/json"

        mock_get.return_value = mock_resp

        add_symbol("IBM")
        # Run the backtest
        result = backtest("IBM", initial_amt, 2, 3)

        # Check expected values
        self.assertEqual(result.trades, expectedTrades)
        self.assertEqual(result.total_return, expectedReturn)
        self.assertEqual(result.max_drawdown, expectedDrawdown)
        self.assertTrue(result.portfolio_data.equals(expected))
