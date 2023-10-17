"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
import logging
import datetime
from dateutil.parser import parse
from unittest import TestCase
from service import app
from decimal import Decimal
from service.models import db
from service.common import status  # HTTP Status Codes
from tests.factories import PromotionFactory
from service.models import Promotion


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

    # def test_create_promotion_route(self):
    #     fake_promotion = PromotionFactory()
    #     # promotion = Promotion(
    #     #     # name=fake_promotion.name,
    #     #     # code=fake_promotion.code,
    #     #     # start=fake_promotion.start,
    #     #     # expired=fake_promotion.expired,
    #     #     # whole_store=fake_promotion.whole_store,
    #     #     # promo_type=fake_promotion.promo_type,
    #     #     # value=fake_promotion.value,
    #     # )

    #     # Convert the 'start' and 'expired' fields to ISO-formatted strings
    #     promotion_data = fake_promotion.serialize()
    #     promotion_data["start"] = promotion_data["start"].isoformat()
    #     promotion_data["expired"] = promotion_data["expired"].isoformat()

    #     # Assuming promotion_data has Decimal values
    #     for key, value in promotion_data.items():
    #         if isinstance(value, Decimal):
    #             promotion_data[key] = float(value)

    #     # Send a POST request to the /promotion route with the modified data
    #     response = self.client.post(
    #         "/promotion",
    #         data=json.dumps(promotion_data),
    #         content_type="application/json",
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     response_data = json.loads(response.data.decode("utf-8"))

    #     # Verify that the response data matches the expected data
    #     self.assertEqual(response_data, promotion_data)

    # def test_bad_path_post_promotion(self):
    #     # Define a sample JSON data to send in the POST request
    #     fake_promotion = PromotionFactory()
    #     data = fake_promotion.serialize()

    #     # Send a POST request to a non-existing path
    #     response = self.client.post(
    #         "/promotions", data=json.dumps(data), content_type="application/json"
    #     )

    #     # Check the response status code
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_404_not_found(self):
        response = self.client.get("/nonexistent_route")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Not Found")
