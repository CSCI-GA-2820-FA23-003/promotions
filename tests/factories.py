"""
Test Factory to make fake objects for testing
"""
from datetime import date, timedelta

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDecimal
from service.models import Promotion


class PromotionFactory(factory.Factory):
    """Creates fake promotions"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""
        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("catch_phrase")
    code = factory.Faker("uuid4")
    start = FuzzyDate(date.today() - timedelta(days=30))
    expired = FuzzyDate(date.today(), date.today() + timedelta(days=30))
    whole_store = FuzzyChoice(choices=[True, False])
    promo_type = FuzzyChoice(choices=[
                                    "B2G1",
                                    "50%OFF",
                                    "30%OFF",
                                    ])
    value = FuzzyDecimal(0.1, 100.0)
