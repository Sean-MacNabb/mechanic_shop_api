from flask import Flask

from application.extensions import db, ma
from application.blueprints.customer import customer_bp
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.service_ticket import service_ticket_bp


def create_app(config_name='config.DevelopmentConfig'):
    """Application factory: builds and configures a Flask app instance."""
    app = Flask(__name__)
    app.config.from_object(config_name)

    # Initialize extensions with this app instance
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints, each prefixed with the plural resource name
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    return app
