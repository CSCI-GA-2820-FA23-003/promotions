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

    def test_update_promotion(self):
        """Update a Promotion's attributes"""
        # Create a promotion using the factory
        promotion = PromotionFactory()
        promotion.create()
        self.assertIsNotNone(promotion.id)

        # Update the promotion
        updated_name = "UpdatedTestPromotion"
        promotion.name = updated_name
        promotion.update()

        # Fetch the updated promotion and verify
        fetched_promotion = Promotion.find(promotion.id)
        self.assertIsNotNone(fetched_promotion)
        self.assertEqual(fetched_promotion.name, updated_name)

    def test_update_promotion_multiple_attributes(self):
        """Update multiple attributes of a Promotion using the factory"""
        promotion = PromotionFactory()
        promotion.create()

        # Update multiple attributes
        updated_data = {"name": "UpdatedName", "whole_store": False, "value": 50}
        for key, value in updated_data.items():
            setattr(promotion, key, value)
        promotion.update()

        # Fetch and verify
        fetched_promotion = Promotion.find(promotion.id)
        for key, value in updated_data.items():
            self.assertEqual(getattr(fetched_promotion, key), value)

    def test_update_promotion_subset_fields_factory(self):
        """Update a subset of a Promotion's attributes using factory"""
        promotion = PromotionFactory(whole_store=True, value=10)
        promotion.create()

        # Update subset of attributes
        updated_data = {"name": "UpdatedSubsetField", "value": 20}
        for key, value in updated_data.items():
            setattr(promotion, key, value)
        promotion.update()

        # Fetch and verify
        fetched_promotion = Promotion.find(promotion.id)
        for key, value in updated_data.items():
            self.assertEqual(getattr(fetched_promotion, key), value)

        # Ensure other fields are not affected
        self.assertTrue(fetched_promotion.whole_store)

    def test_concurrent_updates(self):
        promotion1 = PromotionFactory()
        promotion1.create()

        promotion2 = Promotion.find(promotion1.id)

        promotion1.name = "NameFromFirstProcess"
        promotion2.name = "NameFromSecondProcess"

        promotion1.update()
        promotion2.update()

        fetched_promotion = Promotion.find(promotion1.id)
        self.assertNotEqual(
            fetched_promotion.name, "NameFromFirstProcess"
        )  # Due to race condition, the second process overwrites the first one

    def test_update_with_special_characters(self):
        promotion = PromotionFactory(name="InitialName")
        promotion.create()

        special_name = "NameWithSpecialChars@#^&*()"
        promotion.name = special_name
        promotion.update()

        fetched_promotion = Promotion.find(promotion.id)
        self.assertEqual(fetched_promotion.name, special_name)

    def test_update_after_delete(self):
        promotion = PromotionFactory()
        promotion.create()

        # Check if promotion exists after creation
        fetched_promotion = Promotion.find(promotion.id)
        print(f"Promotion after creation: {fetched_promotion}")

        promotion.delete()

        # Check if promotion exists after deletion
        fetched_promotion = Promotion.find(promotion.id)
        print(f"Promotion after deletion: {fetched_promotion}")

        with self.assertRaises(
            DataValidationError
        ):  # Assuming update throws an error if the record doesn't exist
            promotion.update()
