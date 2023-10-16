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

    # TODO: Please define the rest cases here (delete, update etc.)
    def test_list_all_promotions(self):
        """It should List all Wishlists in the database"""
        promitions = Promotion.all()
        self.assertEqual(promitions, [])
        # Create 5 Pets
        for _ in range(5):
            promotion = PromotionFactory()
            promotion.create()
        # See if we get back 5 pets
        pets = Promotion.all()
        self.assertEqual(len(pets), 5)