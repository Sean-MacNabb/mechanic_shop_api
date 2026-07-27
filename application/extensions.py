from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# These are created here (not inside create_app) so blueprints and models
# can import them without causing circular imports
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
