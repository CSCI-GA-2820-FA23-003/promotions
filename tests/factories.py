"""
Test Factory to make fake objects for testing
"""
from datetime import datetime, timedelta, timezone
import factory
from factory.fuzzy import FuzzyChoice, FuzzyNaiveDateTime, FuzzyDecimal
from service.models import Promotion

EST = timezone(timedelta(hours=-5))


class PromotionFactory(factory.Factory):
    """Creates fake promotions"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    name = factory.Faker("catch_phrase")
    code = factory.Faker("uuid4")
    start = FuzzyNaiveDateTime(
        datetime.utcnow(),
        datetime.utcnow() + timedelta(days=30),
    )
    expired = FuzzyNaiveDateTime(
        datetime.utcnow(),
        datetime.utcnow() + timedelta(days=30),
    )
    whole_store = FuzzyChoice(choices=[True, False])
    promo_type = factory.Sequence(lambda n: (n % 5) + 1)
    value = FuzzyDecimal(0.1, 100.0)
