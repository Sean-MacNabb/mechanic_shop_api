from flask import Blueprint

# Blueprint grouping all inventory-related routes together
inventory_bp = Blueprint('inventory_bp', __name__)

# Imported at the bottom to avoid circular imports
from application.blueprints.inventory import routes
