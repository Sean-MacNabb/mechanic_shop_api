import os

# python-dotenv is only installed locally (it's intentionally excluded from
# requirements.txt) — Render's production environment injects env vars
# directly, so it never needs this package. Guard the import so startup
# doesn't crash in production.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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


class ProductionConfig:
    """Configuration used in the live/production deployment on Render.

    Does NOT inherit from Config, since the base class hardcodes a local
    MySQL URI — production instead reads its Postgres URL straight from
    the environment variable Render injects (and that we set locally
    in .env for testing the config before deploying).
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    CACHE_TYPE = "SimpleCache"