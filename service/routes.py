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
    """Root URL response
    {
        '/': 'The index endpoint. Lists all the other endpoints.',
        '/create': 'POST: creating a promotion.',
        '/read': 'GET: reading a promotion.',
        '/update': 'PUT: updating a promotion',
        '/list': 'GET: to view all existing promotions.',
        '/delete': 'DELETE: deleting an existing promotion.',
    }
    """
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
    Creates a Promotion
    This endpoint will create a Promotion based on the data in the request body.
    """

    # Ensure the request contains JSON data
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")

    # Get the JSON data from the request
    data = request.get_json()

    # Create a new Promotion with the data
    try:
        promotion = Promotion()
        promotion.deserialize(data)
        promotion.create()
    except DataValidationError as error:
        return jsonify({"error": str(error)}), status.HTTP_400_BAD_REQUEST

    app.logger.info("Promotion with ID [%s] created.", promotion.id)

    # Return the new Promotion as JSON
    return (jsonify(promotion.serialize()), status.HTTP_201_CREATED)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


# Place your REST API code here ...

# -----------------------------------------------------------
# Create promotions
# -----------------------------------------------------------
@app.route("/promotion", methods=["POST"])
def create_promotions():
    """Creates a new promotion and stores it in the database"""
    app.logger.info(f"Request to Create a promotion")

    # Create a new Promotion instances
    promo = Promotion()

    # Deserialize the request data and create the promotion
    json_data = request.get_json()
    promo.deserialize(json_data)
    promo.create()

    # Return the created promotion as a JSON response with a 201 status code
    result = promo.serialize()
    return jsonify(result), status.HTTP_201_CREATED

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


def not_found(error):
    """Handle 404 Not Found error with a JSON response."""
    return jsonify({"error": "Not Found", "message": str(error)}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed error with a JSON response."""
    return jsonify({"error": "Method Not Allowed", "message": str(error)}), 405
