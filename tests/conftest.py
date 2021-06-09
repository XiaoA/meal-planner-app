import pytest
from project import create_app, database
from flask import current_app
from project.models import User, UserProfile


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

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
        user = User('batman@example.com', 'password', 'password')
        yield user    
    

    
