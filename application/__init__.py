from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from application.extensions import db, ma, limiter, cache
from application.blueprints.customer import customer_bp
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.service_ticket import service_ticket_bp
from application.blueprints.inventory import inventory_bp

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic Shop API"}
)

def create_app(config_name='config.DevelopmentConfig'):
    """Application factory: builds and configures a Flask app instance."""
    app = Flask(__name__)
    app.config.from_object(config_name)

    # Initialize extensions with this app instance
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register blueprints, each prefixed with the plural resource name
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
