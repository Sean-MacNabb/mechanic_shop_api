from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache


class Base(DeclarativeBase):
    pass


# These are created here (not inside create_app) so blueprints and models
# can import them without causing circular imports
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

# Limits requests based on the client's IP address
limiter = Limiter(key_func=get_remote_address)

# SimpleCache stores cached data in memory, which is fine for development;
# a production app would typically use Redis or another shared cache backend
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
