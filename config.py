import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration with settings shared across all environments."""
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:{os.environ.get('DB_PASSWORD')}@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration used for local development."""
    DEBUG = True


class TestingConfig(Config):
    """Configuration used when running automated tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:{os.environ.get('DB_PASSWORD')}@localhost/mechanic_shop_test_db"


class ProductionConfig(Config):
    """Configuration used in a live/production deployment."""
    DEBUG = False
