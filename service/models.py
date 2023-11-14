"""
Models for PromotionModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import null
from service.exceptions import ConfirmationRequiredError

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

# Relationship table for promotion and product
promotion_product = db.Table(
    "promotion_product",
    db.Column("promotion_id", db.Integer, db.ForeignKey("promotion.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("created_at", db.DateTime, nullable=False, default=db.func.now()),
    db.Column("updated_at", db.DateTime, nullable=False, default=db.func.now()),
)


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Promotion.init_db(app)
    Product.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class ResourceConflictError(Exception):
    """Used for the resource already exist"""


class Promotion(db.Model):  # pylint: disable=too-many-instance-attributes
    """
    Class that represents a PromotionModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    start = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    expired = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Integer, nullable=False, default=1)
    whole_store = db.Column(db.Boolean, nullable=False, default=False)
    promo_type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Double, nullable=False, default=0.0)

    # Relationships
    products = db.relationship("Product", secondary=promotion_product, backref="promotions", cascade="all, delete")
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def __repr__(self):
        return f"<PromotionModel {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a PromotionModel to the database
        """
        self.app.logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        # validation
        if self.code is None or self.code == "":
            raise DataValidationError("code attribute is not set")
        if Promotion.find_by_code(self.code).count() > 0:
            raise ResourceConflictError("code already exist")
        if self.name is None or self.name == "":
            raise DataValidationError("name attribute is not set")
        if self.start is None:
            raise DataValidationError("start attribute is not set")
        if self.whole_store is None:
            self.whole_store = False
        if self.promo_type is None:
            raise DataValidationError("promo_type attribute is not set")
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update

        Raises:
            DataValidationError: _description_
            DataValidationError: _description_
            DataValidationError: _description_
            DataValidationError: _description_
        """
        if not self.id or not db.session.get(
            Promotion, self.id
        ):  # Using the updated session.get() method
            raise DataValidationError(f"Promotion with ID {self.id} not found.")
        if self.name is None or self.name == "":
            raise DataValidationError("name attribute is not set")
        if self.start is None:
            raise DataValidationError("start attribute is not set")
        if self.promo_type is None:
            raise DataValidationError("promo_type attribute is not set")
        db.session.commit()

    def delete(self, confirm=False):
        """Removes a PromotionModel from the data store"""
        if not confirm:
            raise ConfirmationRequiredError("Please confirm deletion")

        self.app.logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a PromotionModel into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "start": self.start.isoformat(),
            "expired": self.expired.isoformat(),
            "whole_store": self.whole_store,
            "promo_type": self.promo_type,
            "value": float(self.value),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def deserialize(self, data):
        """
        Deserializes a PromotionModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.code = data["code"]
            self.start = data["start"]
            self.expired = data["expired"]
            self.whole_store = data["whole_store"]
            self.promo_type = data["promo_type"]
            self.value = data["value"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid PromotionModel: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid PromotionModel: body of request contained bad or no data - "
                "Error message: " + error.args[0]
            ) from error
        return self

    @classmethod
    def init_db(cls, _app):
        """Initializes the database session"""
        _app.logger.info("Initializing database")
        cls.app = _app
        db.init_app(cls.app)
        cls.app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the PromotionModels in the database"""
        cls.app.logger.info("Processing all PromotionModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a PromotionModel by it's ID"""
        cls.app.logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all PromotionModels with the given name

        Args:
            name (string): the name of the PromotionModels you want to match
        """
        cls.app.logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def find_by_code(cls, code):
        """Returns all PromotionModels with the given code

        Args:
            code (string): the code of the PromotionModels you want to match
        """
        cls.app.logger.info("Processing name query for %s ...", code)
        return cls.query.filter(cls.code == code)

    # @classmethod
    # def bind_product(cls, promotion_id, product_id):
    #     """Bind a product to a promotion
    #     Args:
    #         promotion_id (int): the id of the promotion
    #         product_id (int): the id of the product
    #     """
    #     promotion = cls.query.get(promotion_id)
    #     if promotion is None:
    #         raise DataValidationError(f"Promotion with id '{id}' was not found.")

    #     if product_id not in promotion.products:
    #         promotion.products.append(product_id)
    #     else:
    #         raise DataValidationError(
    #             f"Product with id '{id}' is already in the promotion."
    #         )
    #     db.session.commit()

    # @classmethod
    # def apply(cls, promotion_id, product_id=None):
    #     """Apply promotion to a product(optional, if not, apply to all products)
    #     Args:
    #         promotion_id (int): the id of the promotion
    #         product_id (int): the id of the product
    #     """
    #     promotion = cls.query.get(promotion_id)
    #     if promotion is None:
    #         raise DataValidationError(f"Promotion with id '{id}' was not found.")

    #     if promotion.available > 0:
    #         promotion.available -= 1
    #         # TODO: switch to promotion type to apply different promotion

    #         if product_id is None:
    #             # apply to all products
    #             if not promotion.whole_store:
    #                 raise DataValidationError(
    #                     f"Promotion with id '{id}' is not a whole store promotion."
    #                 )
    #             if promotion.available > 0:
    #                 promotion.available -= 1
    #                 # TODO: switch to promotion type to apply different promotion
    #                 db.session.commit()
    #             else:
    #                 raise DataValidationError(
    #                     f"Promotion with id '{id}' is not available. Reach the max available usage"
    #                 )
    #         else:
    #             # apply to a product
    #             if product_id not in promotion.products:
    #                 raise DataValidationError(
    #                     f"Product with id '{id}' is not in the promotion."
    #                 )
    #         db.session.commit()
    #     else:
    #         raise DataValidationError(
    #             f"Promotion with id '{id}' is not available. Reach the max available usage"
    #         )


class Product(db.Model):
    """
    Class that represents a ProductModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Relationships
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def __repr__(self):
        return f"<ProductModel {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a PromotionModel to the database
        """
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def delete(self, confirm=False):
        """Removes a PromotionModel from the data store"""
        if not confirm:
            raise ConfirmationRequiredError("Please confirm deletion")

        self.app.logger.info("Deleting Product[id: %s]", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a PromotionModel into a dictionary"""
        return {
            "id": self.id,
            "promotions": [promotion.serialize() for promotion in self.promotions],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def deserialize(self, data):
        """
        Deserializes a PromotionModel from a dictionary
        """
        # bind the promotion to the product
        if "promotions" in data:
            for promotion in data["promotions"]:
                promotion = Promotion.find(promotion["id"])
                if promotion is None:
                    raise DataValidationError(
                        f"Promotion with id '{promotion['id']}' was not found."
                    )
                self.promotions.append(promotion)
        return self

    @classmethod
    def init_db(cls, _app):
        """Initializes the database session"""
        _app.logger.info("Initializing database")
        cls.app = _app
        db.init_app(cls.app)
        cls.app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """Returns all of the PromotionModels in the database"""
        cls.app.logger.info("Processing all PromotionModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a PromotionModel by it's ID"""
        cls.app.logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)
