"""
My Service

Describe what your service does here
"""
from flask import jsonify, request, url_for, abort, make_response
from service.common import status  # HTTP Status Codes
from service.exceptions import ConfirmationRequiredError
from service.models import Promotion, DataValidationError
from datetime import datetime

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Promotion Demo REST API Service",
            version="1.0",
            paths=url_for("list_promotions", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A PROMOTIONS
######################################################################
@app.route("/promotions", methods=["POST"])
def create_promotion():
    """
    Create a new promotion.

    This endpoint creates a new promotion based on the JSON data provided in the request body.

    Returns:
        JSON: The created promotion as JSON.
    """
    app.logger.info("Request to create a promotion")

    # Ensure the request contains JSON data
    if not request.is_json:
        return (jsonify({"error": "Unsupported media type: Request is not JSON"}), 415)

    # Get the JSON data from the request
    data = request.get_json()

    # Create a new Promotion with the data
    promotion = Promotion()
    promotion.deserialize(data)
    promotion.create()

    location_url = url_for("get_promotions", promotion_id=promotion.id, _external=True)
    app.logger.info("Promotion with ID [%s] created.", promotion.id)

    # Return the new Promotion as JSON
    return (
        jsonify(promotion.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# DELETE A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotion(promotion_id):
    try:
        promotion = Promotion.find(promotion_id)
        if promotion is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )

        confirm = request.args.get("confirm", default="false")
        if confirm != "true":
            raise ConfirmationRequiredError(
                "Please confirm deletion by passing the 'confirm' parameter as true."
            )

        promotion = Promotion.find(promotion_id)
        if promotion:
            promotion.delete(True)

        app.logger.info("Promotion with ID [%s] delete complete.", promotion_id)
        return "", status.HTTP_204_NO_CONTENT

    except ConfirmationRequiredError as e:
        abort(status.HTTP_400_BAD_REQUEST, str(e))


######################################################################
# Update promotions
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotion(promotion_id):
    promotion = Promotion.find(promotion_id)
    if promotion is None:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id {promotion_id} was not found.",
        )
    if datetime.now() > promotion.expired:
        app.logger.warning("Received request to update an expired promotion.")
        abort(
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "Updating expired promotions is not supported",
        )
    app.logger.info("Updating promotion with id %s", promotion_id)
    data = request.get_json()
    try:
        promotion.deserialize(data)
    except DataValidationError as e:
        app.logger.warning("Bad request data: %s", str(e))
        abort(status.HTTP_400_BAD_REQUEST, str(e))
    if not request.is_json:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Unsupported media type: Request is not JSON",
        )
    promotion.id = promotion_id
    promotion.update()
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all of the Promotions"""
    app.logger.info("Request for promotion list")
    promotions = Promotion.all()

    results = [p.serialize() for p in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotions(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on it's id
    """
    app.logger.info("Request for promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    app.logger.info("Returning promotion: %s", promotion.name)
    return jsonify(promotion.serialize()), status.HTTP_200_OK

# ######################################################################
# # Apply promotions
# ######################################################################
# @app.route(
#     "/promotions/<int:promotion_id>/apply/<int:product_id>", methods=["PUT", "POST"]
# )
# def apply_promotion(promotion_id, product_id):
#     promotion = Promotion.find(promotion_id)
#     if promotion is None:
#         abort(
#             status.HTTP_404_NOT_FOUND,
#             f"Promotion with id {promotion_id} was not found.",
#         )
#     if datetime.now() > promotion.expired:
#         app.logger.warning("Received request to update an expired promotion.")
#         abort(
#             status.HTTP_405_METHOD_NOT_ALLOWED,
#             "Updating expired promotions is not supported",
#         )

#     # check if product is in the promotion
#     if product_id not in promotion.products:
#         abort(
#             status.HTTP_404_NOT_FOUND,
#             f"Product with id {product_id} is not in the promotion.",
#         )

#     app.logger.info("Updating promotion with id %s", promotion_id)
#     data = request.get_json()

#     try:
#         promotion.deserialize(data)
#     except DataValidationError as e:
#         app.logger.warning("Bad request data: %s", str(e))
#         abort(status.HTTP_400_BAD_REQUEST, str(e))
#     if not request.is_json:
#         abort(
#             status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             "Unsupported media type: Request is not JSON",
#         )

#     promotion.update()
#     return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)
