"""
Test cases for YourResourceModel Model

"""
import datetime
import os
import logging
import unittest

from flask import Flask
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

    def test_create(self):
        """It should always be true"""
        # create a promotion and assert that it exists
        promotion = Promotion(
            code="TestCode",
            name="TestCode",
            start=datetime.date(2020, 1, 1),
            expired=datetime.date(2020, 1, 1),
            whole_store=True,
            promo_type=1,
            value=1,
        )

    # TODO: Please define the rest cases here (delete, update etc.)

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
        self.assertEqual(data["start"], promotion.start)

        self.assertIn("expired", data)
        self.assertEqual(data["expired"], promotion.expired)

        self.assertIn("whole_store", data)
        self.assertEqual(data["whole_store"], promotion.whole_store)

        self.assertIn("promo_type", data)
        self.assertEqual(data["promo_type"], promotion.promo_type)

        self.assertIn("value", data)
        self.assertEqual(data["value"], promotion.value)

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

    def test_find_promotion_by_id(self):
        """It should Find a Promotion by its ID"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        promotion_id = promotions[0].id
        found = Promotion.find(promotion_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, promotion_id)
