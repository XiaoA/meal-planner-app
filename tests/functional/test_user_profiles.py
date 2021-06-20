from project.models import User, UserProfile
from project import mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def test_show_user_profile_logged_in(test_client, log_in_default_user):

    """
    GIVEN a Flask application configured for testing and the default user logged in
    WHEN the '/users/<int:user_id>' page is requested (GET)
    THEN check that the profile for the current user is displayed
    """
    response = test_client.get('/users/<int:user_id>')
    print(response.data)
    print(response.status_code)
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'User Profile' in response.data
    assert b'Account' in response.data
    assert b'Email: andrewflaskdev@gmail.com' in response.data
    assert b'Account Statistics' in response.data
    assert b'Joined on' in response.data
    assert b'Email address' in response.data
    assert b'confirmed' not in response.data
    assert b'Account Actions' in response.data
    assert b'Change Password' in response.data
    assert b'Resend Email Confirmation' in response.data

def test_show_user_profile_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/<int:user_id>' page is requested (GET) when the user is NOT logged in
    THEN check that the user is redirected to the login page
    """
    response = test_client.get('/users/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'User Profile!' not in response.data
    assert b'Email: andrewflaskdev@gmail.com' not in response.data
    assert b'Please log in to access this page.' in response.data

def test_show_user_profile_logged_in_email_confirmed(test_client, confirm_email_default_user):
    """
    GIVEN a Flask application configured for testing and the default user logged in
          and their email address is confirmed
    WHEN the '/users/<int:user_id>' page is requested (GET)
    THEN check that profile for the current user is presented

    (This test confirms that the `confirm_email_default_user` fixture works)
    """
    response = test_client.get('/users/<int:user_id>',
                               data={'email': 'andrewflaskdev@gmail.com',
                                     'password_hashed': 'password123',
                                     'email_confirmed': True,
                                     'email_confirmed_on': '2021-06-15 15:23:04.8816'},                               
                               follow_redirects=True)
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'User Profile' in response.data
    assert b'Email: andrewflaskdev@gmail.com' in response.data
    assert b'Account Statistics' in response.data
    assert b'Joined on' in response.data
    assert b'Email address has not been confirmed!' not in response.data
    assert b'Email address confirmed on June 13, 2021' in response.data
    assert b'Account Actions' in response.data
    assert b'Change Password' in response.data
    assert b'Resend Email Confirmation' not in response.data

def test_show_user_profiles_for_all_members(test_client, log_in_default_user):
    """
    GIVEN a Flask application with authenticated users
    WHEN the '/users' page is requested (GET)
    THEN check that authenticated users are visible
    """
    response = test_client.get('/users')
    assert response.status_code == 200
    assert b'andrewflaskdev' in response.data
    assert b'Follow' in response.data

def test_navigation_bar_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET) when the user is logged in
    THEN check that the 'My Account', 'My Profile', 'My Recipe Box', and 'Logout' links are present
    """
    response = test_client.get('/')
    print(response.data)
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'My Account' in response.data
    assert b'My Profile' in response.data
    assert b'My Recipe Box' in response.data
    assert b'Logout' in response.data
    assert b'Register' not in response.data
    assert b'Login' not in response.data

def test_navigation_bar_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET) when the user is not logged in
    THEN check that the 'Register' and 'Login' links are present and links for authenticated users are not
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'Register' in response.data
    assert b'Login' in response.data
    assert b'My Account' not in response.data
    assert b'My Profile' not in response.data
    assert b'My Recipe Box' not in response.data
    assert b'Logout' not in response.data
