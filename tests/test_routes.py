"""
TestPromotionResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
import logging
import datetime

from flask import Flask, jsonify
from dateutil.parser import parse
from unittest import TestCase
from service import app
from service.models import db
from service.common import status
from service.common import status  # HTTP Status Codes
from tests.factories import PromotionFactory
from datetime import datetime, timedelta
from service.models import Promotion

BASE_URL = "/promotions"



######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionResourceModel(TestCase):
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
        
    def test_create(self):
        """It should respond to a proper create with 201 status code and return the data."""
        promo = PromotionFactory()
        data_orig = promo.serialize()

        resp = self.client.post(
            "/promotions", data=json.dumps(data_orig), content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        response_json = resp.get_json()

        # remove all auto created entries in the DB
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

    def test_create_promotion_no_data(self):
        """It should not Create a Promotion with missing data"""
        response = self.client.post("/promotions", json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicated_promotion(self):
        promo = PromotionFactory()
        data_orig = promo.serialize()

        resp = self.client.post(
            "/promotions", data=json.dumps(data_orig), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.post(
            "/promotions", data=json.dumps(data_orig), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
    
    
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

    def test_create_invalid_promotion_data(self):
        # Create a promotion with incomplete or invalid data
        invalid_promotion_data = {
            "name": "Invalid Promotion",
            "code": "INVALIDPROMO",
            "start": "2023-10-01",  # Invalid date format
            "expired": "2023-10-10",
            "whole_store": True,
            "promo_type": "Discount",  # Should be an integer
            "value": "Fifteen",  # Should be a numeric value
        }

        response = self.client.post(
            "/promotions",
            data=invalid_promotion_data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_404_not_found(self):
        response = self.client.get("/nonexistent_route")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Not Found")

    def test_not_allow_method(self):
        """It should return a 405 error when calling a nonexistent method"""
        response = self.client.post("/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
