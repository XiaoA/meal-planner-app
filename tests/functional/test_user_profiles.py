from project.models import User, UserProfile
from project import mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def test_user_profile_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing and the default user logged in
    WHEN the '/users/profile' page is requested (GET)
    THEN check that the profile for the current user is displayed
    """
    response = test_client.get('/users/profile')
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'User Profile' in response.data
    assert b'Email: andrewflaskdev@gmail.com' in response.data
    assert b'Account Statistics' in response.data
    assert b'Joined on' in response.data
    assert b'Email address has not been confirmed!' in response.data
    assert b'Email address confirmed on' not in response.data
    assert b'Account Actions' in response.data
    assert b'Change Password' in response.data
    assert b'Resend Email Confirmation' in response.data

def test_user_profile_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/profile' page is requested (GET) when the user is NOT logged in
    THEN check that the user is redirected to the login page
    """
    response = test_client.get('/users/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'User Profile!' not in response.data
    assert b'Email: andrewflaskdev@gmail.com' not in response.data
    assert b'Please log in to access this page.' in response.data

def test_user_profile_logged_in_email_confirmed(test_client, confirm_email_default_user):
    """
    GIVEN a Flask application configured for testing and the default user logged in
          and their email address is confirmed
    WHEN the '/users/profile' page is requested (GET)
    THEN check that profile for the current user is presented

    (This test confirms that the `confirm_email_default_user` fixture works)
    """
    response = test_client.get('/users/profile')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile' in response.data
    assert b'Email: andrewflaskdev@gmail.com' in response.data
    assert b'Account Statistics' in response.data
    assert b'Joined on' in response.data
    assert b'Email address has not been confirmed!' not in response.data
    assert b'Email address confirmed on June 13, 2021' in response.data
    assert b'Account Actions' in response.data
    assert b'Change Password' in response.data
    assert b'Resend Email Confirmation' not in response.data
