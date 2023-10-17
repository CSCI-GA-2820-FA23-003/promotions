"""
Test cases for YourResourceModel Model

"""
import datetime
import os
import logging
import unittest

from flask import Flask
from tests.factories import PromotionFactory
from service.models import Promotion, DataValidationError, db
from service.exceptions import ConfirmationRequiredError
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
        self.assertAlmostEqual(
            float(promotion.value), float(fake_promotion.value), places=2
        )
    
    def test_create_promotion_with_missing_data(self):
        """Test creating a promotion with missing data."""
        fake_promotion = PromotionFactory()
        promotion = Promotion(
            name=fake_promotion.name,
            start=fake_promotion.start,
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            promo_type=fake_promotion.promo_type,
            value=fake_promotion.value,
        )
        self.assertRaises(DataValidationError, promotion.create)

    def test_concurrent_creates(self):
        # Test concurrent creation of promotions
        promotion1 = PromotionFactory()
        promotion2 = PromotionFactory()

        # Create promotions concurrently
        promotion1.create()
        promotion2.create()

        # Check if both promotions were created successfully
        self.assertIsNotNone(promotion1.id)
        self.assertIsNotNone(promotion2.id)

    def test_create_with_special_characters(self):
        # Test creating a promotion with special characters in the name
        special_name = "NameWithSpecialChars@#^&*()"
        promotion = PromotionFactory(name=special_name)

        promotion.create()

        # Check if the promotion was created with the special name
        fetched_promotion = Promotion.find(promotion.id)
        self.assertEqual(fetched_promotion.name, special_name)

    # def test_create_after_delete(self):
    #     # Test creating a promotion after deletion
    #     promotion = PromotionFactory()
    #     promotion.create()

    #     # Check if the promotion exists after creation
    #     fetched_promotion = Promotion.find(promotion.id)
    #     self.assertIsNotNone(fetched_promotion)

    #     promotion.delete()

    #     # Check if the promotion does not exist after deletion
    #     fetched_promotion = Promotion.find(promotion.id)
    #     self.assertIsNone(fetched_promotion)

    #     # Attempt to create the promotion again
    #     promotion.create()

    #     # Check if the promotion was created again
    #     fetched_promotion = Promotion.find(promotion.id)
    #     self.assertIsNotNone(fetched_promotion)

    def test_create_with_deserialize(self):
        # Test creating a promotion using the deserialize method
        create_data = {
            "name": "NewPromotion",
            "code": "CODE123",
            "start": "2023-01-01",
            "expired": "2023-02-01",
            "whole_store": True,
            "promo_type": 1,
            "value": 10.0,
        }

        promotion = PromotionFactory()
        promotion.deserialize(create_data)
        promotion.create()

        # Check if the promotion was created with the provided data
        fetched_promotion = Promotion.find(promotion.id)
        self.assertEqual(fetched_promotion.name, create_data["name"])
        self.assertEqual(fetched_promotion.code, create_data["code"])
        self.assertEqual(fetched_promotion.start, datetime.date(2023, 1, 1))
        self.assertEqual(fetched_promotion.expired, datetime.date(2023, 2, 1))
        self.assertTrue(fetched_promotion.whole_store)
        self.assertEqual(fetched_promotion.promo_type, 1)
        self.assertEqual(fetched_promotion.value, 10.0)
        self.assertIsNotNone(fetched_promotion.id)
        self.assertIsNotNone(fetched_promotion.created_at)
        self.assertIsNotNone(fetched_promotion.updated_at)

    def test_delete_with_confirmation(self):
        """Ensure a promotion cannot be deleted without confirmation"""
        promotion = Promotion(
            code="TestCode",
            name="TestName",
            start=datetime.date(2022, 1, 1),
            expired=datetime.date(2022, 12, 31),
            whole_store=True,
            promo_type=1,
            value=10,
        )
        promotion.create()

        # Ensure promotion is added
        self.assertEqual(len(Promotion.all()), 1)

        # Attempt to delete without confirmation and expect an error
        with self.assertRaises(ConfirmationRequiredError):
            promotion.delete(confirm=False)

        # Ensure promotion is still present after failed delete
        self.assertEqual(len(Promotion.all()), 1)

        # Delete with confirmation
        promotion.delete(confirm=True)

        # Ensure promotion is permanently removed from the system
        self.assertEqual(len(Promotion.all()), 0)
