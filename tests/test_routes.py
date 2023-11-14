"""
TestPromotionResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
import logging

from unittest import TestCase
from datetime import datetime, timedelta
from service import app
from service.models import db, Promotion, init_db, promotion_product, Product
from service.common import status  # HTTP Status Codes
from tests.factories import PromotionFactory, ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI")
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
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(promotion_product).delete()
        db.session.query(Product).delete()
        db.session.query(Promotion).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

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
        """It should update a promotion"""
        # Create a test promotion using the factory
        promotion = PromotionFactory()
        promotion.create()

        # Update the promotion with valid data, including 'created_at'
        updated_data = {
            "name": "Updated Promotion Name",
            "code": promotion.code,
            "start": datetime.now().isoformat(),
            "expired": (datetime.now() + timedelta(days=1)).isoformat(),
            "whole_store": False,
            "promo_type": 1,  # Use a valid integer value for promo_type
            "value": 10.0,
            "created_at": datetime.now().isoformat(),  # Include 'created_at' field
            "updated_at": datetime.now().isoformat(),  # Include 'created_at' field
        }

        response = self.client.put(
            f"/promotions/{promotion.id}",
            data=json.dumps(updated_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_promotion_not_found(self):
        """It should return a 404 error if the promotion doesn't exist"""
        invalid_promotion_id = 99999999
        response = self.client.put(f"/promotions/{invalid_promotion_id}")
        self.assertEqual(response.status_code, 404)

    def test_bad_request(self):
        """It should return a 400 error if the data is invalid"""
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
        """It should return a 405 error if the promotion is expired"""
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
        """It should return a 415 error if the media type is unsupported"""
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
        """It should return a 400 error if the user doesn't confirm deletion"""
        # Create a promotion using the factory
        promotion = PromotionFactory()
        db.session.add(promotion)
        db.session.commit()

        response = self.client.delete(f"/promotions/{promotion.id}")
        self.assertEqual(response.status_code, 400)  # Expected Bad Request
        self.assertIn("Please confirm deletion", response.get_data(as_text=True))

    def test_delete_promotion_success(self):
        """It should delete a promotion if the user confirms deletion"""
        # Assuming we have a method to create a test promotion and return its ID
        promotion_id = self._create_promotions(1)[0].id

        # Delete the promotion
        response = self.client.delete(f"/promotions/{promotion_id}?confirm=true")

        # Check if promotion was successfully deleted
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")

        # Check if the promotion no longer exists
        promotion = Promotion.find(promotion_id)
        self.assertIsNone(promotion)

    def test_delete_promotion_no_confirm(self):
        """It should not delete a promotion if the user doesn't confirm deletion"""
        # Assuming we have a method to create a test promotion and return its ID
        promotion_id = self._create_promotions(1)[0].id

        # Try to delete the promotion without confirmation
        response = self.client.delete(f"/promotions/{promotion_id}?confirm=false")

        # Check if deletion was prevented and a BadRequest was returned
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please confirm deletion", response.get_data(as_text=True))

        # Check that the promotion still exists in the database
        promotion = Promotion.find(promotion_id)
        self.assertIsNotNone(promotion)

    def test_delete_nonexistent_promotion(self):
        """It should return a 404 error if the promotion doesn't exist"""
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
        """It should not Create a duplicated Promotion"""
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
        """It should not Create a Promotion with invalid data"""
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
        """It should return a 404 error if the promotion doesn't exist"""
        response = self.client.get("/nonexistent_route")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Not Found")

    def test_get_promotion_list(self):
        """It should Get a list of promotions"""
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 0)

        self._create_promotions(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_not_allow_method(self):
        """It should return a 405 error when calling a nonexistent method"""
        response = self.client.post("/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_promotion(self):
        """It should Get a single Promotion"""
        # get the id of a promotion
        test_promotion = self._create_promotions(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_promotion.name)

    def test_get_promotion_not_found(self):
        """It should not Get a Promotion thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    # +++++ Actions Routes +++++
    def test_bind_product_to_promotion(self):
        """It should bind a product to a promotion"""
        # Create a promotion
        promotion = PromotionFactory()
        promotion.create()

        # Create a product
        product = ProductFactory()
        product.create()

        # Bind the product to the promotion
        response = self.client.put(f"{BASE_URL}/{promotion.id}/{product.id}")
        self.assertEqual(response.status_code, 200)

    def test_bind_product_to_promotion_promotion_not_found(self):
        """It should not bind a product to a promotion that doesn't exist"""
        # Create a product
        product = ProductFactory()
        product.create()

        # Bind the product to the promotion
        response = self.client.put(f"{BASE_URL}/0/{product.id}")
        self.assertEqual(response.status_code, 404)

    def test_bind_product_to_promotion_product_not_found(self):
        """It should create a product and bind it to a promotion"""
        # Create a promotion
        promotion = PromotionFactory()
        promotion.create()

        # Bind the product to the promotion
        response = self.client.put(f"{BASE_URL}/{promotion.id}/0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(promotion.products), 1)

    def test_apply_promotion(self):
        """It should apply the promotion"""
        promotion = PromotionFactory()
        promotion.start = datetime.now() - timedelta(days=1)
        promotion.available = 1
        promotion.create()
        response = self.client.post(f"{BASE_URL}/{promotion.id}/apply")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(promotion.available, 0)

    def test_apply_nonexistent_promotion(self):
        """It should not apply the promotion"""
        response = self.client.post(f"{BASE_URL}/0/apply")
        self.assertEqual(response.status_code, 404)

    def test_apply_inactive_promotion(self):
        """It should not apply the promotion"""
        promotion = PromotionFactory()
        promotion.start = datetime.now() + timedelta(days=1)
        promotion.create()
        response = self.client.post(f"{BASE_URL}/{promotion.id}/apply")
        self.assertEqual(response.status_code, 405)

    def test_apply_expired_promotion(self):
        """It should not apply the promotion"""
        promotion = PromotionFactory()
        promotion.expired = datetime.now() - timedelta(days=1)
        promotion.create()
        response = self.client.post(f"{BASE_URL}/{promotion.id}/apply")
        self.assertEqual(response.status_code, 405)

    def test_apply_unavailable_promotion(self):
        """It should not apply the promotion"""
        promotion = PromotionFactory()
        promotion.available = 0
        promotion.create()
        response = self.client.post(f"{BASE_URL}/{promotion.id}/apply")
        self.assertEqual(response.status_code, 405)
