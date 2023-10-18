"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Promotion, DataValidationError
from flask import make_response

# Import Flask application
from . import app
from datetime import datetime


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
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

    app.logger.info("Promotion with ID [%s] created.", promotion.id)

    # Return the new Promotion as JSON
    return (jsonify(promotion.serialize()), 201)


@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotion(promotion_id):
    """Delete a promotion and requires confirmation"""
    promotion = Promotion.find(promotion_id)
    if promotion is None:
        abort(
            status.HTTP_404_NOT_FOUND,
            "Promotion with id {} was not found.".format(promotion_id),
        )

    confirm = request.args.get("confirm", default=False, type=bool)

    if confirm:
        promotion.delete()
        return make_response(jsonify({}), status.HTTP_204_NO_CONTENT)
    else:
        abort(
            status.HTTP_400_BAD_REQUEST,
            "Please confirm deletion by passing the 'confirm' parameter as true.",
        )

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
    if datetime.now().date() > promotion.expired:
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
