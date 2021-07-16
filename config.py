import os
import re
from datetime import timedelta

API_BASE_URL = "https://api.spoonacular.com"
API_INGREDIENT_SEARCH_URL = " https://api.spoonacular.com/recipes/complexSearch"
API_KEY = os.getenv('API_KEY', default='')

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='DEV_SECREt_KEY')

    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        default="postgresql:///meal_planner_app").replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    # Flask Mail Config
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY', default='')

class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL',
                                        default="postgresql:///meal_planner_app_test")
    SECRET_KEY = os.getenv('SECRET_KEY', default='')
    
