from project.models import User, UserProfile
from project import mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def test_get_password_reset_via_email_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email' page is requested (GET)
    THEN check that the page is successfully returned
    """
    response = test_client.get('/users/password_reset_via_email', follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Reset via Email' in response.data
    assert b'Email' in response.data
    assert b'Submit' in response.data

def test_post_password_reset_via_email_page_valid(test_client, confirm_email_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email' page is posted to (POST) with a valid email address
    THEN check that an email was queued up to send
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/users/password_reset_via_email',
                                    data={'email': 'andrewflaskdev@gmail.com'},
                                    follow_redirects=True)
        assert response.status_code == 200
        assert b'Please check your email for a password reset link.' in response.data
        assert len(outbox) == 1
        assert outbox[0].subject == 'Recipie App - Password Reset Requested'
        assert outbox[0].sender == 'flaskrecipieapp@gmail.com'
        assert outbox[0].recipients[0] == 'andrewflaskdev@gmail.com'
        assert 'Questions? Comments?' in outbox[0].html
        assert 'flaskrecipieapp@gmail.com' in outbox[0].html
        assert 'http://localhost/users/password_reset_via_token/' in outbox[0].html    

def test_post_password_reset_via_email_page_invalid(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email' page is posted to (POST) with an invalid email address
    THEN check that an error message is flashed
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/users/password_reset_via_email',
                                    data={'email': 'andrewflaskdev'},
                                    follow_redirects=True)
        assert response.status_code == 200
        print(response.data)
        assert len(outbox) == 0
        assert b'validation-error' in response.data
        assert b'Invalid email address.' in response.data

def test_post_password_reset_via_email_page_not_confirmed(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email' page is posted to (POST) with a email address that has not been confirmed
    THEN check that an error message is flashed
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/users/password_reset_via_email',
                                    data={'email': 'andrewflaskdev@gmail.com'},
                                    follow_redirects=True)
        assert response.status_code == 200
        assert len(outbox) == 0
        assert b'Your email address must be confirmed before attempting a password reset.' in response.data

def test_get_password_reset_valid_token(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email/<token>' page is requested (GET) with a valid token
    THEN check that the page is successfully returned
    """
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = password_reset_serializer.dumps('andrewflaskdev@gmail.com', salt='password-reset-salt')

    response = test_client.get('/users/password_reset_via_token/' + token, follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Reset' in response.data
    assert b'New Password' in response.data
    assert b'Submit' in response.data
       
def test_get_password_reset_invalid_token(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email/<token>' page is requested (GET) with an invalid token
    THEN check that an error message is displayed
    """
    token = 'invalid_token'

    response = test_client.get('/users/password_reset_via_token/' + token, follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Reset' not in response.data
    assert b'The password reset link is invalid or has expired.' in response.data

def test_post_password_reset_valid_token(test_client, afterwards_reset_default_user_password):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email/<token>' page is posted to (POST) with a valid token
    THEN check that the password provided is processed
    """
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = password_reset_serializer.dumps('andrewflaskdev@gmail.com', salt='password-reset-salt')

    response = test_client.post('/users/password_reset_via_token/' + token,
                                data={'password': 'mynewestpassword99'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Your password has been updated!' in response.data

def test_post_password_reset_invalid_token(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/password_reset_via_email/<token>' page is posted to (POST) with an invalid token
    THEN check that the password provided is processed
    """
    token = 'invalid_token'

    response = test_client.post('/users/password_reset_via_token/' + token,
                                data={'password': 'My#Strongerx7&Passw0rd98!'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Your password has been updated!' not in response.data
    assert b'The password reset link is invalid or has expired.' in response.data    


def test_get_change_password_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing with the user logged in
    WHEN the '/users/change_password' page is retrieved (GET)
    THEN check that the page is retrieved successfully
    """
    response = test_client.get('/users/change_password', follow_redirects=True)
    assert response.status_code == 200
    assert b'Change Password' in response.data
    assert b'Current Password' in response.data
    assert b'New Password' in response.data

def test_get_change_password_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing with the user NOT logged in
    WHEN the '/users/change_password' page is retrieved (GET)
    THEN check an error message is returned to the user
    """
    response = test_client.get('/users/change_password', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Change Password' not in response.data

def test_post_change_password_logged_in_valid_current_password(test_client, log_in_default_user, afterwards_reset_default_user_password):
    """
    GIVEN a Flask application configured for testing with the user logged in
    WHEN the '/users/change_password' page is posted to (POST) with the correct current password
    THEN check that the user's password is updated correctly
    """
    response = test_client.post('/users/change_password',
                                data={'current_password': 'password123',
                                      'new_password': 'newpassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Your password has been updated!' in response.data
    user = User.query.filter_by(email='andrewflaskdev@gmail.com').first()
    assert not user.is_password_correct('password123')
    assert user.is_password_correct('newpassword123')

def test_post_change_password_logged_in_invalid_current_password(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing with the user logged in
    WHEN the '/users/change_password' page is posted to (POST) with the incorrect current password
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/change_password',
                                data={'current_password': 'wrongpassword123',
                                      'new_password': 'newpassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Password has been updated!' not in response.data
    assert b'ERROR! Incorrect user credentials!' in response.data
 
def test_post_change_password_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing with the user not logged in
    WHEN the '/users/change_password' page is posted to (POST)ho
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/change_password',
                                data={'current_password': 'password123',
                                      'new_password': 'newpassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Password has been updated!' not in response.data   
