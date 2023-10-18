"""
Models for PromotionModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from service.exceptions import ConfirmationRequiredError
from . import app

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Promotion.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""
    
class ResourceConflictError(Exception):
    """Used for the resource already exist"""


class Promotion(db.Model):
    """
    Class that represents a PromotionModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    start = db.Column(db.Date, nullable=False)
    expired = db.Column(db.Date)
    whole_store = db.Column(db.Boolean, nullable=False, default=False)
    promo_type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Double, nullable=True)
    created_at = db.Column(db.Date, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.Date,
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
        app.logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        # validation
        if self.code is None:
            raise DataValidationError("code attribute is not set")
        
        # find if code is already exist
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
        if self.value is None:
            self.value = 0.0  
        db.session.add(self)
        db.session.commit()

    def update(self):
        if not self.id or not db.session.get(
            Promotion, self.id
        ):  # Using the updated session.get() method
            raise DataValidationError("Promotion with ID {} not found.".format(self.id))
        
        if self.name is None or self.name == "":
            raise DataValidationError("name attribute is not set")
        if self.start is None:
            raise DataValidationError("start attribute is not set")
        if self.whole_store is None:
            self.whole_store = False
        if self.promo_type is None:
            raise DataValidationError("promo_type attribute is not set")
        if self.value is None:
            self.value = 0.0
        db.session.commit()

    def delete(self, confirm=False):
        """Removes a PromotionModel from the data store"""
        if not confirm:
            raise ConfirmationRequiredError("Please confirm deletion")

        app.logger.info("Deleting %s", self.name)
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
    def init_db(cls, app):
        """Initializes the database session"""
        app.logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the PromotionModels in the database"""
        app.logger.info("Processing all PromotionModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a PromotionModel by it's ID"""
        app.logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


    @classmethod
    def find_by_name(cls, name):
        """Returns all PromotionModels with the given name

        Args:
            name (string): the name of the PromotionModels you want to match
        """
        app.logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()
    
    @classmethod
    def find_by_code(cls, code):
        """Returns all PromotionModels with the given code

        Args:
            code (string): the code of the PromotionModels you want to match
        """
        app.logger.info("Processing name query for %s ...", code)
        return cls.query.filter(cls.code == code)
