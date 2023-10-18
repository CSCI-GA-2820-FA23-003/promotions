"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort, make_response, Flask
from service.common import status  # HTTP Status Codes
from service.models import Promotion, DataValidationError

# Import Flask application
from . import app


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


######################################################################
# Create promotions
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
