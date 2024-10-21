from django.db import models
from financial_data.models import Symbol

# Create your models here.


class Predictions(models.Model):
    """
    This class models the predictions of the ai model
    """

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    date = models.DateField()
    prediction = models.FloatField()

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

    def __str__(self):
        return f"{self.symbol} - {self.date}"
