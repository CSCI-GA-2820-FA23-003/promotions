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
from urllib.parse import quote_plus
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
        """Create a Promotion and then update it"""
        # Create a test promotion using the factory
        promotion = PromotionFactory()
        promotion.create()

        # Update the promotion with valid data, including 'created_at'
        updated_data = {
            "name": "Updated Promotion Name",
            "code": promotion.code,
            "start": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "expired": (datetime.now() + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "whole_store": False,
            "promo_type": 1,  # Use a valid integer value for promo_type
            "value": 10.0,
            "created_at": datetime.now().isoformat(),  # Include 'created_at' field
            "updated_at": datetime.now().isoformat(),  # Include 'created_at' field
            "available": 10,
        }

        response = self.client.put(
            f"/promotions/{promotion.id}",
            data=json.dumps(updated_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_promotion_not_found(self):
        """It should return a 404 error if a Promotion is not found by id"""
        invalid_promotion_id = 99999999
        response = self.client.put(f"/promotions/{invalid_promotion_id}")
        self.assertEqual(response.status_code, 404)

    def test_bad_request(self):
        """It should return 400 Bad Request if the data is invalid"""
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
        """It should not update an expired Promotion"""
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
        """It should return 415 Unsupported Media Type when Content-Type is not supported"""
        promotion = PromotionFactory()
        promotion.create()
        promotion.update()

        response = self.client.put(
            f"/promotions/{promotion.id}",  # Use a valid promotion ID
            data="<xml>Data</xml>",
            content_type="application/xml",
        )

        self.assertEqual(response.status_code, 415)

    def test_delete_promotion_success(self):
        """
        Test the deletion of a non-expired promotion. The test verifies that the
        response status code is 204, indicating that the operation was successful.
        """
        # Create a new promotion that is not expired
        promotion = Promotion(
            code="PROMO123",
            name="Test Promotion",
            start=datetime.utcnow(),
            expired=datetime.utcnow() + timedelta(days=1),
            whole_store=False,
            promo_type=1,
            value=10.0,
        )

        db.session.add(promotion)
        db.session.commit()

        response = self.client.delete(f"/promotions/{promotion.id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_promotion(self):
        """It should return a 404 error if a Promotion is not found by id"""
        response = self.client.delete("/promotions/999999")
        self.assertEqual(response.status_code, 404)

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
        """It should return a 404 error if a Promotion is not found by id"""
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

    def test_query_promotion_list_by_name(self):
        """It should Query Promotion by Name"""
        promotions = self._create_promotions(10)
        test_name = promotions[0].name
        name_promotions = [
            promotion for promotion in promotions if promotion.name == test_name
        ]
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(name_promotions))
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["name"], test_name)

    def test_query_promotion_list_by_code(self):
        """It should Query Promotion by Code"""
        promotions = self._create_promotions(10)
        test_code = promotions[0].code
        code_promotions = [
            promotion for promotion in promotions if promotion.code == test_code
        ]
        response = self.client.get(
            BASE_URL, query_string=f"code={quote_plus(test_code)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(code_promotions))
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["code"], test_code)

    def test_query_promotion_list_by_promo_type(self):
        """It should Query Promotion by Promo_type"""
        promotions = self._create_promotions(10)
        test_promo_type = promotions[0].promo_type
        promo_type_promotions = [
            promotion
            for promotion in promotions
            if promotion.promo_type == test_promo_type
        ]
        response = self.client.get(
            BASE_URL, query_string=f"promo_type={test_promo_type}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(promo_type_promotions))
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["promo_type"], test_promo_type)

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

    def test_unbind_product_from_promotion(self):
        """It should unbind a product from a promotion"""
        # Create a promotion
        promotion = PromotionFactory()
        promotion.create()

        # Create a product
        product = ProductFactory()
        product.create()

        # Bind the product to the promotion
        response = self.client.put(f"{BASE_URL}/{promotion.id}/{product.id}")
        self.assertEqual(response.status_code, 200)

        # Unbind the product from the promotion
        response = self.client.delete(f"{BASE_URL}/{promotion.id}/{product.id}")
        self.assertEqual(response.status_code, 200)

    def test_unbind_product_from_promotion_promotion_not_found(self):
        """It should not unbind a product from a promotion that doesn't exist"""
        # Create a product
        product = ProductFactory()
        product.create()

        # Unbind the product from the promotion
        response = self.client.delete(f"{BASE_URL}/0/{product.id}")
        self.assertEqual(response.status_code, 404)

    def test_unbind_nonexistent_product_from_promotion(self):
        """It should not unbind a nonexistent product from a promotion"""
        # Create a promotion
        promotion = PromotionFactory()
        promotion.create()

        # Unbind the product from the promotion
        response = self.client.delete(f"{BASE_URL}/{promotion.id}/0")
        self.assertEqual(response.status_code, 405)

    def test_unbind_nonbound_product_from_promotion(self):
        """It should not unbind a nonbound product from a promotion"""
        # Create a promotion
        promotion = PromotionFactory()
        promotion.create()

        # Create a product
        product = ProductFactory()
        product.create()

        # Unbind the product from the promotion
        response = self.client.delete(f"{BASE_URL}/{promotion.id}/{product.id}")
        self.assertEqual(response.status_code, 405)

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

    def test_cancel_promotion(self):
        """It should cancel the promotion"""
        promotion = PromotionFactory()
        promotion.available = 0
        promotion.create()
        response = self.client.post(f"{BASE_URL}/{promotion.id}/cancel")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(promotion.available, 0)

    def test_cancel_nonexistent_promotion(self):
        """It should not cancel the promotion"""
        response = self.client.post(f"{BASE_URL}/0/cancel")
        self.assertEqual(response.status_code, 404)

    def test_edit_View(self):
        """It should edit the promotion"""
        promotion = PromotionFactory()
        promotion.create()
        response = self.client.get(f"promotion/{promotion.id}/edit")
        self.assertEqual(response.status_code, 200)

    def test_edit_nonexistent_promotion(self):
        """It should not edit the promotion"""
        response = self.client.get(f"{BASE_URL}/0/edit")
        self.assertEqual(response.status_code, 404)
