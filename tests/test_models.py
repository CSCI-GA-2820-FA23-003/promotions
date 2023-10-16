"""
Test cases for YourResourceModel Model

"""
import datetime
import os
import logging
import unittest

from flask import Flask
from service.models import Promotion, DataValidationError, db
from tests.factories import PromotionFactory


######################################################################
#  PromotionModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionResourceModel(unittest.TestCase):
    """Test Cases for PromotionModel Model"""

    @classmethod
    def setUpClass(cls):
        DATABASE_URI = os.getenv("DATABASE_URI")

        """This runs once before the entire test suite"""
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        Promotion.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_promotion(self):
        """Test creating a promotion."""
        promotion = Promotion()
        promotion_data = {
            "code": "Promo1",
            "name": "Promo1",
            "start": datetime.date(2020, 1, 1),
            "expired": datetime.date(2020, 1, 1),
            "whole_store": True,
            "promo_type": 1,
            "value": 1,
            # "created_at": datetime.datetime.now(),
            # "updated_at": datetime.datetime.now(),
        }
        promotion.deserialize(promotion_data)
        promotion.create()
        self.assertIsNotNone(promotion.id)
        self.assertEqual(promotion.name, "Promo1")

    def test_create_promotion_with_valid_data(self):
        """Test creating a promotion with valid data."""
        fake_promotion = PromotionFactory()
        promotion = Promotion(
            name=fake_promotion.name,
            code=fake_promotion.code,
            start=fake_promotion.start,
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            promo_type=fake_promotion.promo_type,
            value=fake_promotion.value,
        )
        promotion.create()
        self.assertIsNotNone(promotion.id)
        self.assertEqual(promotion.name, fake_promotion.name)
        self.assertEqual(promotion.code, fake_promotion.code)
        self.assertEqual(promotion.start, fake_promotion.start)
        self.assertEqual(promotion.expired, fake_promotion.expired)
        self.assertEqual(promotion.whole_store, fake_promotion.whole_store)
        self.assertEqual(promotion.promo_type, fake_promotion.promo_type)
        self.assertEqual(str(promotion.value), str(fake_promotion.value))

    def test_create_promotion_with_existing_code(self):
        # Test creating a promotion with an existing code should raise a DataValidationError.
        existing_promotion = PromotionFactory()
        promotion_data = {
            "name": "NewPromotion",
            "code": existing_promotion.code,
            "start": datetime.date(2021, 1, 1),
            "expired": datetime.date(2021, 12, 31),
            "whole_store": False,
            "promo_type": 8,
            "value": 10.0,
        }
        promotion = Promotion()
        try:
            promotion.deserialize(promotion_data)
            promotion.create()
        except DataValidationError as e:
            print(f"DataValidationError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    # # TODO: Please define the rest cases here (delete, update etc.)
