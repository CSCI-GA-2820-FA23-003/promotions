"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db
from service.common import status
from tests.factories import PromotionFactory
from service.models import Promotion


# HTTP Status Codes


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceServer(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """This runs after each test"""

    def _create_promotions(self, count):
        """Creates promotions for testing"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            test_promotion.create()
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_promotion_without_confirmation(self):
        # Create a promotion using the factory
        promotion = PromotionFactory()
        db.session.add(promotion)
        db.session.commit()

        response = self.client.delete(f"/promotions/{promotion.id}")
        self.assertEqual(response.status_code, 400)  # Expected Bad Request
        self.assertIn("Please confirm deletion", response.get_data(as_text=True))

    # def test_delete_promotion_with_confirmation(self):
    # Create a promotion using the factory
    # promotion = PromotionFactory()
    # db.session.add(promotion)
    # db.session.commit()

    # response = self.client.delete(f"/promotions/{promotion.id}?confirm=true")
    # self.assertEqual(response.status_code, 204)  # Expected No Content

    def test_delete_nonexistent_promotion(self):
        # Attempt to delete a promotion that doesn't exist
        response = self.client.delete("/promotions/999999?confirm=true")
        self.assertEqual(response.status_code, 404)  # Expected Not Found
        self.assertIn("was not found", response.get_data(as_text=True))
