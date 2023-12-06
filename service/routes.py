"""
My Service

Describe what your service does here
"""
from datetime import datetime, date
from flask import request, render_template, jsonify
from flask_restx import Resource, fields, reqparse
from service.common import status  # HTTP Status Codes
from service.models import Promotion, DataValidationError, Product
from . import app, api

# Define the model for Promotion
create_model = api.model(
    "Promotion",
    {
        "code": fields.String(required=True, description="Unique promotion code"),
        "name": fields.String(required=True, description="Name of the promotion"),
        "start": fields.DateTime(
            required=True, description="Start date and time of the promotion"
        ),
        "expired": fields.DateTime(
            required=True, description="Expiration date and time of the promotion"
        ),
        "available": fields.Integer(
            required=True, description="Availability status of the promotion"
        ),
        "whole_store": fields.Boolean(
            required=True, description="Is the promotion applicable to the whole store?"
        ),
        "promo_type": fields.Integer(
            required=True, description="Type of the promotion"
        ),
        "value": fields.Float(required=True, description="Value of the promotion"),
        "products": fields.List(
            fields.Integer,
            description="List of product IDs associated with the promotion",
        ),
        "created_at": fields.DateTime(
            description="Creation date and time of the promotion"
        ),
        "updated_at": fields.DateTime(
            description="Last update date and time of the promotion"
        ),
    },
)
# query string arguments
promotion_args = reqparse.RequestParser()
promotion_args.add_argument(
    "name", type=str, location="args", required=False, help="List Promotions by name"
)
promotion_args.add_argument(
    "code", type=str, location="args", required=False, help="List Promotions by code"
)
promotion_args.add_argument(
    "promo_type",
    type=int,
    location="args",
    required=False,
    help="List Promotions by promo_type",
)


create_product_model = api.model(
    "Product",
    {
        "id": fields.Integer(required=True, description="Name of the product"),
        "created_at": fields.DateTime(
            description="Creation date and time of the product"
        ),
        "updated_at": fields.DateTime(
            description="Last update date and time of the product"
        ),
    },
)

promotion_model = api.inherit(
    "PromotionModel",
    create_model,
    {
        "id": fields.String(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

product_model = api.inherit(
    "ProductModel",
    create_product_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

product_args = reqparse.RequestParser()
product_args.add_argument(
    "id", type=int, location="args", required=True, help="The existing product id"
)

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Index page"""
    return app.send_static_file("index.html")


######################################################################
# Health Check Endpoint
# Returns status OK for Kubernetes health check
######################################################################


@app.route("/health", methods=["GET"])
def health():
    """health check"""
    return jsonify({"status": "OK"}), 200


######################################################################
# Promotions User View
######################################################################


@app.route("/promotions/<int:promotion_id>/edit", methods=["GET"])
def promotion_detail_view(promotion_id):
    """Root URL response"""
    app.logger.info("Request for Root URL")
    promotion = Promotion.find(promotion_id)
    pruducts = Product.all()

    if promotion is None:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id {promotion_id} was not found.",
        )

    bind_products = [
        {
            "id": product.id,
            "selected": product in promotion.products,
        }
        for product in pruducts
    ]
    return render_template(
        "promotion.html", promotion=promotion, products=bind_products
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# PATH: /products
######################################################################


@api.route("/products", strict_slashes=False)
class ProductCollection(Resource):
    """Handles all interactions with collections of Products"""

    ######################################################################
    # LIST ALL PRODUCTS
    ######################################################################
    @api.doc("list_products")
    @api.marshal_list_with(promotion_model)
    def get(self):
        """Returns all of the Products"""
        app.logger.info("Request for product list")
        products = Product.all()
        results = [p.serialize() for p in products]
        app.logger.info("Returning %d products", len(results))
        return results, status.HTTP_200_OK

    ######################################################################
    # CREATE A PRODUCT
    ######################################################################
    @api.doc("create_products")
    @api.response(400, "The posted data was not valid")
    @api.response(415, "Unsupported media type")
    @api.expect(create_product_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Create a new product.

        This endpoint creates a new product based on the JSON data provided in the request body.

        Returns:
            JSON: The created product as JSON.
        """
        app.logger.info("Request to create a product")

        # Get the JSON data from the request
        data = api.payload

        # Create a new Product with the data
        product = Product()
        product.deserialize(data)
        product.create()

        app.logger.info("Product with ID [%s] created.", product.id)

        # Return the new Product as JSON
        return (
            product.serialize(),
            status.HTTP_201_CREATED,
        )


######################################################################
# PATH: /product/<int:product_id>
######################################################################


@api.route("/products/<int:product_id>")
@api.param("product_id", "The Product identifier")
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Product
    GET /{product_id} - Returns a Product with the id
    """

    ######################################################################
    # DELETE A PRODUCT
    ######################################################################

    @api.doc("delete_products")
    @api.response(204, "Product deleted")
    @api.response(404, "Product not found")
    def delete(self, product_id):
        """
        Delete a product by its ID.

        This function removes a product from the database if it exists.
        If the product does not exist, a 404 error is returned.

        Args:
            product_id (int): Unique identifier of the product to be deleted.

        Returns:
            tuple: An empty string and a status code of 204 indicating successful deletion.
        """
        product = Product.find(product_id)

        if product is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id {product_id} was not found.",
            )

        app.logger.info("Deleting product with id %s", product_id)
        product.delete()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
# PATH: /promotions
######################################################################


@api.route("/promotions", strict_slashes=False)
class PromotionCollection(Resource):
    """Handles all interactions with collections of Promotions"""

    ######################################################################
    # CREATE A PROMOTIONS
    ######################################################################
    @api.doc("create_promotions")
    @api.response(400, "The posted data was not valid")
    @api.response(415, "Unsupported media type")
    @api.expect(create_model)
    @api.marshal_with(promotion_model, code=201)
    def post(self):
        """
        Create a new promotion.

        This endpoint creates a new promotion based on the JSON data provided in the request body.

        Returns:
            JSON: The created promotion as JSON.
        """
        app.logger.info("Request to create a promotion")

        # Get the JSON data from the request
        data = api.payload

        # Create a new Promotion with the data
        promotion = Promotion()
        promotion.deserialize(data)
        promotion.create()

        location_url = api.url_for(
            PromotionResource, promotion_id=promotion.id, _external=True
        )
        app.logger.info("Promotion with ID [%s] created.", promotion.id)

        # Return the new Promotion as JSON
        return (
            promotion.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )

    ######################################################################
    # LIST ALL PROMOTIONS
    ######################################################################

    @api.doc("list_promotions")
    @api.expect(promotion_args, validate=True)
    @api.marshal_list_with(promotion_model)
    def get(self):
        """Returns all of the Promotions"""
        app.logger.info("Request for promotion list")
        args = promotion_args.parse_args()
        name = args["name"]
        code = args["code"]
        promo_type = args["promo_type"]

        if name:
            promotions = Promotion.find_by_name(name)
        elif code:
            promotions = Promotion.find_by_code(code)
        elif promo_type:
            promotions = Promotion.find_by_promo_type(promo_type)
        else:
            promotions = Promotion.all()

        results = [p.serialize() for p in promotions]
        app.logger.info("Returning %d promotions", len(results))
        return results, status.HTTP_200_OK


######################################################################
# PATH: /promotions/<int:promotion_id>
######################################################################


@api.route("/promotions/<int:promotion_id>")
@api.param("promotion_id", "The Promotion identifier")
class PromotionResource(Resource):
    """
    PromotionResource class

    Allows the manipulation of a single Promotion
    GET /{promotion_id} - Returns a Promotion with the id
    PUT /{promotion_id} - Update a Promotion with the id
    DELETE /{promotion_id} -  Deletes a Promotion with the id
    """

    ######################################################################
    # DELETE A PROMOTION
    ######################################################################
    @api.doc("delete_promotions")
    @api.response(204, "Promotion deleted")
    def delete(self, promotion_id):
        """
        Delete a promotion by its ID.

        This function removes a promotion from the database if it exists and has not expired.
        If the promotion does not exist, a 404 error is returned.
        If the promotion has expired, a 405 error is returned indicating that deletion of expired promotions is not supported.

        Args:
            promotion_id (int): Unique identifier of the promotion to be deleted.

        Returns:
            tuple: An empty string and a status code of 204 indicating successful deletion.
        """
        promotion = Promotion.find(promotion_id)

        if promotion is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )

        app.logger.info("Deleting promotion with id %s", promotion_id)
        promotion.delete()

        return "", status.HTTP_204_NO_CONTENT

    ######################################################################
    # Update A Promotion
    ######################################################################
    @api.doc("update_promotions")
    @api.response(404, "Promotion not found")
    @api.response(400, "Bad request")
    @api.expect(promotion_model)
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        """Update a Promotion

        This endpoint will update a Promotion based the body that is posted
        Args:
            promotion_id (int): ID of the promotion to update
        Returns:
            json: The promotion that was updated
        """
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )
        if date.today() > promotion.expired:
            app.logger.warning("Received request to update an expired promotion.")
            abort(
                status.HTTP_405_METHOD_NOT_ALLOWED,
                "Updating expired promotions is not supported",
            )
        app.logger.info("Updating promotion with id %s", promotion_id)
        data = api.payload
        try:
            promotion.deserialize(data)
        except DataValidationError as error:
            app.logger.warning("Bad request data: %s", str(error))
            abort(status.HTTP_400_BAD_REQUEST, str(error))
        if not request.is_json:
            abort(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "Unsupported media type: Request is not JSON",
            )
        promotion.id = promotion_id
        promotion.update()
        return (promotion.serialize(), status.HTTP_200_OK)

    ######################################################################
    # RETRIEVE A PROMOTION
    ######################################################################

    @api.doc("get_promotions")
    @api.response(404, "Promotion not found")
    @api.marshal_with(promotion_model)
    def get(self, promotion_id):
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
        return promotion.serialize(), status.HTTP_200_OK


######################################################################
# PATH: /promotions/<int:promotion_id>/apply
######################################################################


@api.route("/promotions/<int:promotion_id>/apply")
@api.param("promotion_id", "The Promotion identifier")
class PromotionApply(Resource):
    """Apply action on a Promotion"""

    ######################################################################
    # Apply Promotion
    ######################################################################
    @api.doc("apply_promotion")
    @api.response(404, "Promotion not found")
    @api.response(405, "Promotion cannot be applied")
    def post(self, promotion_id):
        """Apply the promotion

        Args:
            promotion_id (inr): Promotion ID

        Returns:
            json: The data of the promotion
        """
        promotion = Promotion.find(promotion_id)

        if promotion is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )
        if date.today() > promotion.expired:
            app.logger.warning("Received request to apply an expired promotion.")
            abort(
                status.HTTP_405_METHOD_NOT_ALLOWED,
                "Applying expired promotions is not supported",
            )
        elif date.today() < promotion.start:
            app.logger.warning("Received request to apply an Inactive promotion.")
            abort(
                status.HTTP_405_METHOD_NOT_ALLOWED,
                "Applying Inactive promotions is not supported",
            )

        if promotion.available == 0:
            app.logger.warning("Received request to apply an unavailable promotion.")
            abort(
                status.HTTP_405_METHOD_NOT_ALLOWED,
                "Applying unavailable promotions is not supported, reach the limit of promotion",
            )

        app.logger.info("Applying promotion with id %s", promotion_id)
        promotion.available -= 1
        promotion.update()
        return (promotion.serialize(), status.HTTP_200_OK)


######################################################################
# Cancel A Promotion
######################################################################


@api.route("/promotions/<int:promotion_id>/cancel")
@api.param("promotion_id", "The Promotion identifier")
class PromotionCancel(Resource):
    """Cancel action on a Promotion"""

    @api.doc("cancel_promotion")
    @api.response(404, "Promotion not found")
    def post(self, promotion_id):
        """Cancel the promotion
        Args:
            promotion_id (int): Promotion ID

        Returns:
            json: The data of the promotion
        """
        promotion = Promotion.find(promotion_id)
        if promotion is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )
        app.logger.info("Canceling promotion with id %s", promotion_id)
        promotion.invalidate()
        return (promotion.serialize(), status.HTTP_200_OK)


######################################################################
# PATH: /promotions/<int:promotion_id>/bind/<int:product_id>
######################################################################


@api.route("/promotions/<int:promotion_id>/bind/<int:product_id>")
class PromotionBindProduct(Resource):
    """Binding action on a Promotion"""

    ######################################################################
    # Bind Product to Promotion
    ######################################################################
    @api.doc("bind_product_to_promotion")
    @api.response(404, "Promotion or Product not found")
    @api.response(409, "Product already in promotion")
    def put(self, promotion_id, product_id):
        """Bind the product to the current promotion

        Args:
            promotion_id (int): Promotion ID
            product_id (int): Product ID

        Returns:
            Promotion: the new promotion with the bound product
        """
        promotion = Promotion.find(promotion_id)

        if promotion is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )
        # check if product is in the promotion
        product = Product.find(product_id)
        if product is None:
            product = Product(id=product_id)
            product.create()
            promotion.products.append(product)
        elif product in promotion.products:
            abort(
                status.HTTP_409_CONFLICT,
                f"Product with id {product_id} is already in the promotion.",
            )
        else:
            promotion.products.append(product)

        app.logger.info("Updating promotion with id %s", promotion_id)
        return (promotion.serialize(), status.HTTP_200_OK)


######################################################################
# PATH: /promotions/<int:promotion_id>/unbind/<int:product_id>
######################################################################


@api.route("/promotions/<int:promotion_id>/unbind/<int:product_id>")
class PromotionUnbindProduct(Resource):
    """Unbinding action on a Promotion"""

    ######################################################################
    # Unbind Product from Promotion
    ######################################################################
    @api.doc("unbind_product_from_promotion")
    @api.response(404, "Promotion or Product not found")
    @api.response(409, "Product not in promotion")
    def delete(self, promotion_id, product_id):
        """Unbind the product from the current promotion

        Args:
            promotion_id (int): Promotion ID
            product_id (int): Product ID

        Returns:
            Promotion: the new promotion without the unbound product
        """
        promotion = Promotion.find(promotion_id)

        if promotion is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id {promotion_id} was not found.",
            )
        # check if product is in the promotion
        product = Product.find(product_id)
        if product is None:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id {product_id} was not found.",
            )
        elif product not in promotion.products:
            abort(
                status.HTTP_409_CONFLICT,
                f"Product with id {product_id} is not in the promotion.",
            )
        else:
            promotion.products.remove(product)

        app.logger.info("Updating promotion with id %s", promotion_id)
        return (promotion.serialize(), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


def init_db(dbname="promotions"):
    """Initialize the model"""
    Promotion.init_db(dbname)


def data_reset():
    """Removes all Promotions from the database"""
    Promotion.remove_all()
