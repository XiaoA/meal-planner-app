from project.models import User, UserProfile
from project import mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def test_get_registration_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/register')
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'User Registration' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data

def test_first_user_follows_second_user(test_client, log_in_default_user):
    """
    GIVEN a Flask application with two autheticated users
    WHEN the '/users/follow' page is requested (POST)
    THEN check the response is valid and follower/following relationship has been created
    """
    response = test_client.get('/users/follow')
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'You are now following secondaryuser' in response.data

def test_first_user_unfollows_second_user(test_client, log_in_default_user):
    """
    GIVEN a Flask application with two autheticated users
    WHEN the '/users/unfollow' page is requested (POST)
    THEN check the response is valid and follower/following relationship has been created
    """
    response = test_client.get('/users/follow')
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'You are no longer following secondaryuser' in response.data    
