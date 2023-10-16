"""
Models for PromotionModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Promotion.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Promotion(db.Model):
    """
    Class that represents a PromotionModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(63))
    start = db.Column(db.Date)
    expired = db.Column(db.Date)
    whole_store = db.Column(db.Boolean)
    promo_type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Double)
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
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    # def update(self):
    #     """
    #     Updates a PromotionModel to the database
    #     """
    #     logger.info("Saving %s", self.name)
    #     db.session.commit()
    def update(self):
        if not self.id or not db.session.get(
            Promotion, self.id
        ):  # Using the updated session.get() method
            raise DataValidationError("Promotion with ID {} not found.".format(self.id))
        db.session.commit()

    def delete(self):
        """Removes a PromotionModel from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a PromotionModel into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "start": self.start,
            "expired": self.expired,
            "whole_store": self.whole_store,
            "promo_type": self.promo_type,
            "value": self.value,
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

            if data["created_at"]:
                self.created_at = data["created_at"]
            else:
                self.created_at = db.func.current_timestamp()
            if data["updated_at"]:
                self.updated_at = data["updated_at"]
            else:
                self.updated_at = db.func.current_timestamp()
        except KeyError as error:
            raise DataValidationError(
                "Invalid PromotionModel: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid PromotionModel: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the PromotionModels in the database"""
        logger.info("Processing all PromotionModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a PromotionModel by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all PromotionModels with the given name

        Args:
            name (string): the name of the PromotionModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
