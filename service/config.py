"""
Global Configuration for Application
"""
import os

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:pgs3cr3t@postgres:5432/promotionstore"
)

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "pgs3cr3t")
