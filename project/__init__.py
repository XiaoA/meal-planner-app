from flask import Flask
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import os

def register_app_callbacks(app):
    @app.before_request
    def app_before_request():
        app.logger.info('Calling before_request() for the Flask application...')

    @app.after_request
    def app_after_request(response):
        app.logger.info('Calling after_request() for the Flask application...')
        return response

    @app.teardown_request
    def app_teardown_request(error=None):
        app.logger.info('Calling teardown_request() for the Flask application...')

    @app.teardown_appcontext
    def app_teardown_appcontext(error=None):
        app.logger.info('Calling teardown_appcontext() for the Flask application...')
        
def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Configure the Flask app
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object('config.DevelopmentConfig')

    register_blueprints(app)
    configure_logging(app)
    register_app_callbacks(app)
    return app

def register_blueprints(app):
    # Import the blueprints
    from project.recipes import recipes_blueprint
    from project.users import users_blueprint

    # Register the blueprints
    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')

def configure_logging(app):
    # Remove the default Flask logger
    app.logger.removeHandler(default_handler)

    # Configure custom logging
    file_handler = RotatingFileHandler('instance/recipie.log',
                                       maxBytes=16384,
                                       backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Log application startup event
    app.logger.info('Starting Recipie App...')




