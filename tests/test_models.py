"""
Test cases for YourResourceModel Model

"""
from datetime import datetime
import os
import logging
import unittest

from flask import Flask
from tests.factories import PromotionFactory
from service.models import Promotion, DataValidationError, db
from service.exceptions import ConfirmationRequiredError


######################################################################
#  PromotionModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionResourceModel(unittest.TestCase):
    """Test Cases for PromotionModel Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
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
        self.assertIsNotNone(promotion.start, fake_promotion.start)
        self.assertIsNotNone(promotion.expired, fake_promotion.expired)
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
        )
        self.assertRaises(DataValidationError, promotion.create)

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

        # Call delete with confirmation
        promotion.delete(confirm=True)

        # Check if promotion exists after deletion
        fetched_promotion = Promotion.find(promotion.id)
        print(f"Promotion after deletion: {fetched_promotion}")

        with self.assertRaises(
            DataValidationError
        ):  # Assuming update throws an error if the record doesn't exist
            promotion.update()

    def test_update_with_deserialize(self):
        promotion = PromotionFactory()
        promotion.create()

        # We're omitting 'created_at' and 'updated_at' from update_data.
        # They will be automatically set by the `deserialize` method.
        update_data = {
            "name": 12345,  # It's strange to have a numeric name. Consider changing this if it's not intentional.
            "code": "NEWCODE",
            "start": datetime(2022, 1, 1).isoformat(),
            "expired": datetime(2022, 2, 1).isoformat(),
            "whole_store": False,
            "promo_type": 2,
            "value": 50.0,
        }

        promotion.deserialize(update_data)

        # Assuming the `update` method saves the changes to the database
        promotion.update()

        fetched_promotion = Promotion.find(promotion.id)
        self.assertIsNotNone(fetched_promotion.created_at)

    def test_update_reflected_in_all_promotions(self):
        """Test that an updated promotion reflects the changes when fetched using the all method"""

        promotion1 = PromotionFactory()
        promotion2 = PromotionFactory()
        db.session.add(promotion1)
        db.session.add(promotion2)
        db.session.commit()

        original_name = promotion2.name

        new_name = "UpdatedName"
        promotion2.name = new_name
        promotion2.update()

        promotions = Promotion.all()

        updated_promotion = next(
            (promo for promo in promotions if promo.id == promotion2.id), None
        )
        self.assertIsNotNone(
            updated_promotion,
            "Updated promotion not found in the list fetched by all method.",
        )
        self.assertEqual(
            updated_promotion.name,
            new_name,
            "Updated promotion name doesn't match the expected name.",
        )

        unchanged_promotion = next(
            (promo for promo in promotions if promo.id == promotion1.id), None
        )
        self.assertIsNotNone(
            unchanged_promotion,
            "Original promotion not found in the list fetched by all method.",
        )
        self.assertNotEqual(
            unchanged_promotion.name,
            original_name,
            "Original promotion name seems to have changed, which is unexpected.",
        )

    def test_update_name_and_retrieve(self):
        """After updating the name of a promotion, it should be retrievable by the new name"""

        promotion = PromotionFactory(name="OriginalName")
        db.session.add(promotion)
        db.session.commit()

        promotion.name = "UpdatedName"
        promotion.update()

        # Validation
        retrieved_promotions = Promotion.find_by_name("UpdatedName")
        self.assertEqual(len(retrieved_promotions), 1)
        self.assertEqual(retrieved_promotions[0].id, promotion.id)

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
            expired=fake_promotion.expired,
            whole_store=fake_promotion.whole_store,
            promo_type=fake_promotion.promo_type,
            value=fake_promotion.value,
        )
        self.assertRaises(DataValidationError, promotion.create)

    def test_create_with_deserialize(self):
        # Test creating a promotion using the deserialize method
        create_data = {
            "name": "NewPromotion",
            "code": "CODE123",
            "start": "2023-01-01 00:00:00",
            "expired": "2023-02-01 00:00:00",
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
        self.assertEqual(fetched_promotion.start, datetime(2023, 1, 1))
        self.assertEqual(fetched_promotion.expired, datetime(2023, 2, 1))
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

        self.assertEqual(data["start"], promotion.start.isoformat())

        self.assertIn("expired", data)
        self.assertEqual(data["expired"], promotion.expired.isoformat())

        self.assertIn("whole_store", data)
        self.assertEqual(data["whole_store"], promotion.whole_store)

        self.assertIn("promo_type", data)
        self.assertEqual(data["promo_type"], promotion.promo_type)

        self.assertIn("value", data)
        self.assertEqual(float(data["value"]), float(promotion.value))

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
