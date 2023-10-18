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
from service.models import Promotion, DataValidationError


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
    def test_repr(self):
        """Test the string representation of the PromotionModel."""
        promotion = Promotion(name="SamplePromotion")
        promotion.id = 123  # Assuming id is set separately, if not adjust accordingly

        expected_repr = "<PromotionModel SamplePromotion id=[123]>"
        self.assertEqual(repr(promotion), expected_repr)

    def test_list_all_promotions(self):
        """It should List all Wishlists in the database"""
        promitions = Promotion.all()
        self.assertEqual(promitions, [])
        # Create 5 Promotions
        for _ in range(5):
            promotion = PromotionFactory()
            promotion.create()
        # See if we get back 5 promotions
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 5)

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

    def test_create_promotion_without_name(self):
        """Test creating a promotion without a name."""
        fake_promotion = PromotionFactory(name=None)
        promotion = Promotion(
            code=fake_promotion.code,
            start=fake_promotion.start,
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            promo_type=fake_promotion.promo_type,
            value=fake_promotion.value,
        )
        self.assertRaises(DataValidationError, promotion.create)

    def test_create_promotion_without_start(self):
        """Test creating a promotion without a start date."""
        fake_promotion = PromotionFactory(start=None)
        promotion = Promotion(
            name=fake_promotion.name,
            code=fake_promotion.code,
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            promo_type=fake_promotion.promo_type,
            value=fake_promotion.value,
        )
        self.assertRaises(DataValidationError, promotion.create)

    def test_create_promotion_without_whole_store(self):
        """Test creating a promotion without specifying whole_store. It should default to False."""
        fake_promotion = PromotionFactory(whole_store=None)
        promotion = Promotion(
            name=fake_promotion.name,
            code=fake_promotion.code,
            start=fake_promotion.start,
            expired=fake_promotion.expired,
            promo_type=fake_promotion.promo_type,
            value=fake_promotion.value,
        )
        promotion.create()
        self.assertIsNotNone(promotion.id)
        self.assertFalse(promotion.whole_store)  # Assert default value

    def test_create_promotion_without_promo_type(self):
        """Test creating a promotion without a promo_type."""
        fake_promotion = PromotionFactory(promo_type=None)
        promotion = Promotion(
            name=fake_promotion.name,
            code=fake_promotion.code,
            start=fake_promotion.start,
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            value=fake_promotion.value,
        )
        self.assertRaises(DataValidationError, promotion.create)

    def test_create_promotion_without_value(self):
        """Test creating a promotion without a value."""
        fake_promotion = PromotionFactory(value=None)
        promotion = Promotion(
            name=fake_promotion.name,
            code=fake_promotion.code,
            start=fake_promotion.start,
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            promo_type=fake_promotion.promo_type,
        )
        self.assertRaises(DataValidationError, promotion.create)

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

        # Instantiate promotion using the factory
        promotion = PromotionFactory()

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

    def test_serialize_a_promotion(self):
        """It should serialize a Promotion"""
        promotion = PromotionFactory()
        data = promotion.serialize()

        self.assertNotEqual(data, None)

        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)

        self.assertIn("code", data)
        self.assertEqual(data["code"], promotion.code)

        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("start", data)
        self.assertEqual(data["start"], promotion.start.strftime("%Y-%m-%d"))

        self.assertIn("expired", data)
        self.assertEqual(data["start"], promotion.start.strftime("%Y-%m-%d"))

        self.assertIn("whole_store", data)
        self.assertEqual(data["whole_store"], promotion.whole_store)

        self.assertIn("promo_type", data)
        self.assertEqual(data["promo_type"], promotion.promo_type)

        self.assertIn("value", data)
        self.assertEqual(data["value"], float(promotion.value))

        self.assertIn("created_at", data)
        self.assertEqual(data["created_at"], promotion.created_at)

        self.assertIn("updated_at", data)
        self.assertEqual(data["updated_at"], promotion.updated_at)

    def test_deserialize_a_promotion(self):
        """It should de-serialize a Promotion"""
        data = PromotionFactory().serialize()
        promotion = Promotion()
        promotion.deserialize(data)

        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(data["code"], promotion.code)
        self.assertEqual(data["name"], promotion.name)
        self.assertEqual(data["start"], promotion.start)
        self.assertEqual(data["expired"], promotion.expired)
        self.assertEqual(data["whole_store"], promotion.whole_store)
        self.assertEqual(data["promo_type"], promotion.promo_type)
        self.assertEqual(data["value"], promotion.value)

    def test_deserialize_bad_data(self):
        """It should raise a DataValidationError when deserializing bad data."""

        bad_data = "this is not a dictionary"
        promotion = Promotion()
        with self.assertRaises(DataValidationError) as context:
            promotion.deserialize(bad_data)

        self.assertIn(
            "Invalid PromotionModel: body of request contained bad or no data",
            str(context.exception),
        )

    def test_find_promotion_by_id(self):
        """It should Find a Promotion by its ID"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        promotion_id = promotions[0].id
        found = Promotion.find(promotion_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, promotion_id)
