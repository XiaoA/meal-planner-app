import pytest
from project import create_app, database
from flask import current_app
from project.models import User, UserProfile
from datetime import datetime
import requests

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')
    flask_app.extensions['mail'].suppress = True

    # Create a test client using the Flask app testing config
    with flask_app.test_client() as testing_client:

    # Establish an application context manager to set up and clear the Application Context
        with flask_app.app_context():
            current_app.logger.info('In the test_client() fixture...')

    yield testing_client

@pytest.fixture(scope='module')
def new_user():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    # Establish an application context before creating the User object
    with flask_app.app_context():
        user = User('andrewflaskdev@gmail.com', 'password123', 'password123')
        yield user

@pytest.fixture(scope='module')
def register_default_user(test_client):
    # Register the default user
    test_client.post('/users/register',
                     data={'email': 'andrewflaskdev@gmail.com',
                           'password_hashed': 'password123',
                           'password_confirmation_hashed': 'password123',
                           'username': 'abuckingham',
                           'first_name': 'Andrew',
                           'last_name': 'Buckingham'},
                     follow_redirects=True)
    return

@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the default user
    test_client.post('/users/login',
                     data={'email': 'andrewflaskdev@gmail.com',
                           'password': 'password123'},
                     follow_redirects=True)

    yield

    # Log out the default user
    test_client.get('/users/logout', follow_redirects=True)
