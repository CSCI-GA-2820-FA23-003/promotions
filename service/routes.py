"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Promotion

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
