"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
import logging
from unittest import TestCase
from service import app
from service.models import db
from service.common import status  # HTTP Status Codes
from tests.factories import PromotionFactory
import datetime


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

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_valid_promotion(self):
        """Update a Promotion's attributes"""
        # Create a test promotion using the factory
        promotion = PromotionFactory()
        promotion.create()

        # Update promotion through API
        new_name = "UpdatedNameUsingFactory"

        # Assuming the Promotion model has attributes like name, code, start, created_at, etc.
        updated_data = {
            "name": new_name,
            "code": promotion.code,
            "start": str(promotion.start),  # Convert date to string for JSON payload
            "expired": str(
                promotion.expired
            ),  # Convert date to string for JSON payload
            "whole_store": promotion.whole_store,
            "promo_type": promotion.promo_type,
            "value": promotion.value,
            "created_at": str(
                promotion.created_at
            ),  # Convert datetime to string for JSON payload
            "updated_at": str(
                datetime.datetime.utcnow()
            ),  # Set updated_at to current time
        }

        response = self.client.put(
            f"/promotions/{promotion.id}",
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
