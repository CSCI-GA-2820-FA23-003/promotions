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
