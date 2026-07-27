from flask import Blueprint

# Blueprint grouping all customer-related routes together
customer_bp = Blueprint('customer_bp', __name__)

# Imported at the bottom to avoid circular imports, since routes.py
# needs to import customer_bp from this same file
from application.blueprints.customer import routes
