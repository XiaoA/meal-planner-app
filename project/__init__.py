from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from flask_login import LoginManager
from flask_mail import Mail
import os


""" Create instances of the Flask application """
database = SQLAlchemy()
db_migration = Migrate()
bcrypt = Bcrypt()
csrf_protection = CSRFProtect()
login = LoginManager()
login.login_view = "users.login"
mail = Mail()

""" Helper Functions """
def initialize_extensions(app):
    database.init_app(app)
    db_migration.init_app(app, database)
    bcrypt.init_app(app)
    csrf_protection.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    from project.models import User, UserProfile, RecipeBox, Meal

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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
        
def register_blueprints(app):
    # Import the blueprints
    from project.recipes import recipes_blueprint
    from project.users import users_blueprint

    # Register the blueprints
    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(users_blueprint)

def create_app():
    # Create the Flask app

    app = Flask(__name__)
    
    # Configure the Flask app
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)


    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_app_callbacks(app)
    register_error_pages(app)
    return app

def configure_logging(app):
    # Updated Logging Configuaration for Heroku
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
    # Configure custom logging
    file_handler = RotatingFileHandler('instance/recipie.log',
                                       maxBytes=16384,
                                       backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)        

    # Remove the default Flask logger
    app.logger.removeHandler(default_handler)

    # Log application startup event
    app.logger.info('Starting Recipie App...')

    
def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    @app.errorhandler(403)
    def page_forbidden(e):
        return render_template('users/403.html'), 403
