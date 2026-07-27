from flask import Blueprint

# Blueprint grouping all service ticket-related routes together
service_ticket_bp = Blueprint('service_ticket_bp', __name__)

# Imported at the bottom to avoid circular imports, since routes.py
# needs to import service_ticket_bp from this same file
from application.blueprints.service_ticket import routes
