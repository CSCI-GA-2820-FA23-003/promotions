"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort, make_response, Flask
from service.common import status  # HTTP Status Codes
from service.models import Promotion

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


# Place your REST API code here ...


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

######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all of the Promotions"""
    app.logger.info("Request for promotion list")
    promotions = []
    name = request.args.get("name")
    if name:
        promotions = Promotion.find_by_name(name)
    else:
        promotions = Promotion.all()

    results = [p.serialize() for p in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK


# ######################################################################
# # ADD A NEW PROMOTION
# ######################################################################
# @app.route("/promotions", methods=["POST"])
# def create_promotions():
#     """
#     Creates a promotion
#     This endpoint will create a promotion based the data in the body that is posted
#     """
#     app.logger.info("Request to create a promotion")
#     check_content_type("application/json")
#     promotion = Promotion()
#     promotion.deserialize(request.get_json())
#     promotion.create()
#     message = promotion.serialize()
#     location_url = url_for(
#         "create_promotions", promotion_id=promotion.id, _external=True
#     )

#     app.logger.info("promotion with ID [%s] created.", promotion.id)
#     return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


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
