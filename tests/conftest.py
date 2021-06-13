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

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with flask_app.app_context():
            flask_app.logger.info('Creating database tables in test_client fixture...')

            # Create the database and the database table(s)
            database.create_all()

        yield testing_client

        with flask_app.app_context():
            database.drop_all()

@pytest.fixture(scope='module')
def new_user():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    # Establish an application context before creating the User object
    with flask_app.app_context():
        user = User('andrewflaskdev@gmail.com', 'password123')
        yield user

@pytest.fixture(scope='module')
def register_default_user(test_client):
    # Register the default user
    test_client.post('/users/register',
                     data={'email': 'andrewflaskdev@gmail.com',
                           'password_hashed': 'password123',
                           'username': 'andrewflaskdev',
                           'first_name': 'Andrew',
                           'last_name': 'Flaskdev'},
                     follow_redirects=True)
    return

@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the default user
    user = test_client.post('/users/login',
                            data={'email': 'andrewflaskdev@gmail.com',
                                  'password': 'password123'},
                            follow_redirects=True)

    yield

    # Log out the default user
    test_client.get('/users/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def confirm_email_default_user(test_client, log_in_default_user):
    # Mark the user as having their email address confirmed
    user = User.query.filter_by(email='andrewflaskdev@gmail.com').first()
    user.email_confirmed = True
    user.email_confirmed_on = datetime(2020, 7, 8)
    database.session.add(user)
    database.session.commit()

    yield user

    # Mark the user as not having their email address confirmed (clean up)
    user = User.query.filter_by(email='andrewflaskdev@gmail.com').first()
    user.email_confirmed = False
    user.email_confirmed_on = None
    database.session.add(user)
    database.session.commit()

@pytest.fixture(scope='function')
def afterwards_reset_default_user_password():
    yield

    # reset the password back to the default user password
    user = User.query.filter_by(email='andrewflaskdev@gmail.com').first()
    user.set_password('password123')
    database.session.add(user)
    database.session.commit()
    
