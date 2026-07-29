from application import create_app
from application.extensions import db

# Import models so their tables are registered with Base.metadata
# before db.create_all() runs
from application import models

app = create_app('config.ProductionConfig')

with app.app_context():
    db.create_all()