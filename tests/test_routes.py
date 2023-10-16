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
from datetime import datetime, timedelta


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
        # Create a test promotion using the factory
        promotion = PromotionFactory()
        promotion.create()

        # Update the promotion with valid data, including 'created_at'
        updated_data = {
            "name": "Updated Promotion Name",
            "code": promotion.code,
            "start": str(datetime.utcnow()),
            "expired": str(datetime.utcnow() + timedelta(days=1)),
            "whole_store": False,
            "promo_type": 1,  # Use a valid integer value for promo_type
            "value": 10.0,
            "created_at": str(datetime.utcnow()),  # Include 'created_at' field
            "updated_at": str(datetime.utcnow()),  # Include 'created_at' field
        }

        response = self.client.put(
            f"/promotions/{promotion.id}",
            data=json.dumps(updated_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_promotion_not_found(self):
        invalid_promotion_id = 99999999
        response = self.client.put(f"/promotions/{invalid_promotion_id}")
        self.assertEqual(response.status_code, 404)

    def test_bad_request(self):
        invalid_data = {}  # Empty data, which should trigger a bad request
        promotion = PromotionFactory()
        promotion.create()
        response = self.client.put(
            f"/promotions/{promotion.id}",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_expired_promotion(self):
        promotion = PromotionFactory()
        promotion.create()
        promotion.expired = datetime.utcnow() - timedelta(days=1)
        promotion.update()
        updated_data = {}
        response = self.client.put(
            f"/promotions/{promotion.id}",
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 405)

    def test_unsupported_media_type(self):
        promotion = PromotionFactory()
        promotion.create()
        promotion.update()

        response = self.client.put(
            f"/promotions/{promotion.id}",  # Use a valid promotion ID
            data="<xml>Data</xml>",
            content_type="application/xml",
        )

        self.assertEqual(response.status_code, 415)

    # def test_promotion_conflict(self):
    #     promotion1 = PromotionFactory()
    #     promotion1.create()

    #     promotion2 = PromotionFactory()
    #     promotion2.create()

    #     # Assuming a scenario where two promotions cannot have the same 'code'.
    #     # We'll try to update the 'code' of promotion2 to match that of promotion1,
    #     # triggering a conflict.
    #     updated_data = {
    #         "name": promotion1.name,
    #         "code": "some code",  # This should create a conflict
    #         "start": str(datetime.utcnow()),
    #         "expired": str(datetime.utcnow() + timedelta(days=1)),
    #         "whole_store": False,
    #         "promo_type": 1,  # Use a valid integer value for promo_type
    #         "value": 10.0,
    #         "created_at": str(datetime.utcnow()),  # Include 'created_at' field
    #         "updated_at": str(datetime.utcnow()),  # Include 'created_at' field
    #     }

    #     response = self.client.put(
    #         f"/promotions/{promotion2.id}",
    #         data=json.dumps(updated_data),
    #         content_type="application/json",
    #     )

    #     self.assertEqual(response.status_code, 409)
    #     response_data = json.loads(response.data)
    #     self.assertEqual(response_data["error"], "Conflict")
    #     self.assertEqual(
    #         response_data["message"], "The description of the conflict scenario"
    #     )
