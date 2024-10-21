from ai_integration.models import Predictions
from ai_integration.predictor import get_predictions, save_predictions
from django.test import TestCase
from financial_data.models import Symbol

# Create your tests here.


class Test(TestCase):
    def test(self):
        Symbol.objects.create(symbol="IBM")
        predictions = get_predictions("IBM")
        save_predictions("IBM", predictions)
        predictions = Predictions.objects.all()
        self.assertEqual(len(predictions), 30)
