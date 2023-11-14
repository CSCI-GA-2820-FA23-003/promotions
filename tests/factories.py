"""
Test Factory to make fake objects for testing
"""
from datetime import datetime, timedelta, timezone

# from venv import create
import factory
from factory.fuzzy import FuzzyChoice, FuzzyNaiveDateTime, FuzzyDecimal
from service.models import Product, Promotion

EST = timezone(timedelta(hours=-5))


class PromotionFactory(factory.Factory):
    """Creates fake promotions"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    name = factory.Faker("catch_phrase")
    code = factory.Faker("uuid4")
    start = FuzzyNaiveDateTime(
        datetime.now(),
        datetime.now() + timedelta(days=2),
    )
    expired = FuzzyNaiveDateTime(
        datetime.now() + timedelta(days=2, hours=1),
        datetime.now() + timedelta(days=3),
    )
    available = factory.Faker("pyint", min_value=1)
    whole_store = FuzzyChoice(choices=[True, False])
    promo_type = factory.Sequence(lambda n: (n % 5) + 1)
    value = FuzzyDecimal(0.1, 100.0)


class ProductFactory(factory.Factory):
    """Creates fake products"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Faker("pyint", min_value=1)
