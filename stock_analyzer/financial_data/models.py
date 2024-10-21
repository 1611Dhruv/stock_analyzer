from django.db import models


class Symbol(models.Model):
    """
    This table stores the different symbols currently present in our
    database
    """

    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.symbol.__str__()


class FinancialData(models.Model):
    """
    This models the data from the API to be stored in the database
    It is indexed over its 'date' field because we want to access date
    sequentially from the starting date for backtesting
    """

    symbol = models.ForeignKey(
        Symbol, on_delete=models.CASCADE
    )  # Relationship to Symbol model
    date = models.DateField()  # Date of the stock price
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        """
        Makes the symbol and date unique and has an index over symbol and date
        """

        unique_together = (
            "symbol",
            "date",
        )  # Unique constraint on symbol and date for consistency
        indexes = [
            models.Index(fields=["symbol", "date"]),  # Index for optimizing queries
        ]
        ordering = ["symbol", "date"]

    def __str__(self):
        return f"{self.symbol} - {self.date}"
