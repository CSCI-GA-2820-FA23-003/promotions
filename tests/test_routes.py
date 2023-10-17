"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
import json
import logging

from flask import Flask, jsonify
from dateutil.parser import parse
from unittest import TestCase
from service import app
from decimal import Decimal
from decimal import Decimal
from service.models import db
from service.common import status
from tests.factories import PromotionFactory
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
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        """This runs before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """This runs after each test"""

    def _create_promotions(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion",
            )
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create(self):
        """It should respond to a proper create with 201 status code and return the data."""
        promo = PromotionFactory()
        data_orig = promo.serialize()

        resp = self.client.post(
            "/promotions", data=json.dumps(data_orig), content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        response_json = resp.get_json()

        # remove all auto created entries
        if "id" in response_json:
            del response_json["id"]
            del data_orig["id"]

        if "created_at" in response_json:
            del response_json["created_at"]
            del data_orig["created_at"]

        if "updated_at" in response_json:
            del response_json["updated_at"]
            del data_orig["updated_at"]

        self.assertEqual(response_json, data_orig)

    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_create_promotion_no_data(self):
        """It should not Create a Promotion with missing data"""
        response = self.client.post("/promotions", json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """It should not Create a Promotion with no content type"""
        response = self.client.post("/promotions")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_wrong_content_type(self):
        """It should not Create a Promotion with the wrong content type"""
        response = self.client.post(
            "/promotions", data="hello", content_type="text/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # def test_create_promotion_bad_value(self):
    #     """It should not Create a Promotion with bad value data"""
    #     test_promotion = PromotionFactory()
    #     logging.debug(test_promotion)
    #     test_promotion.value = "abc"
    #     response = self.client.post("/promotions", json=test_promotion.serialize())
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_promotion_bad_category(self):
    #     """It should not Create a Promotion with bad category data"""
    #     promotion = PromotionFactory()
    #     logging.debug(promotion)
    #     # Change category to a bad string
    #     test_promotion = promotion.serialize()
    #     test_promotion["whole_store"] = "invalid_category"
    #     response = self.client.post("/promotions", json=test_promotion)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
