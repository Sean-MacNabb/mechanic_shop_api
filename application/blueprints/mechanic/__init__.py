from flask import Blueprint

# Blueprint grouping all mechanic-related routes together
mechanic_bp = Blueprint('mechanic_bp', __name__)

# Imported at the bottom to avoid circular imports, since routes.py
# needs to import mechanic_bp from this same file
from application.blueprints.mechanic import routes
