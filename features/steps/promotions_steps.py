"""
Promotion Steps

Steps file for Promotion.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_404_NOT_FOUND = 404


@given("the following promotions")
def step_impl(context):
    """Delete all Promotions and load new ones"""

    # List all of the promotions and delete them one by one
    rest_endpoint = f"{context.base_url}/api/promotions"
    context.resp = requests.get(rest_endpoint)
    assert (
        context.resp.status_code == HTTP_200_OK
    ), f"Expected 200 OK, got {context.resp.status_code}"
    for promotion in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{promotion['id']}")
        assert (
            context.resp.status_code == HTTP_204_NO_CONTENT
        ), f"Expected 204 No Content, got {context.resp.status_code}"

    # load the database with new promotions
    for row in context.table:
        payload = {
            "code": row["code"],
            "name": row["name"],
            "start": row["start"],
            "expired": row["expired"],
            "available": row["available"],
            "whole_store": row["whole_store"] in ["True", "true", "1"],
            "promo_type": row["promo_type"],
            "value": row["promo_type"],
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert (
            context.resp.status_code == HTTP_201_CREATED
        ), f"Expected 201 Created, got {context.resp.status_code}"
