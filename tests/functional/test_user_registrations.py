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

def test_valid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with valid data
    THEN check the response is valid and the user is registered, and an email is queued to send
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/users/register',
                                    data={'email': 'andrewflaskdev@gmail.com',
                                          'password_hashed': 'password123',
                                          'username': 'andrewflaskdev',
                                          'first_name': 'Andrew',
                                          'last_name': 'Flaskdev'},
                                    follow_redirects=True)
        assert response.status_code == 200
        assert b'Thanks for registering, andrewflaskdev! Please check your email to confirm your email address.' in response.data

        assert len(outbox) == 1
        assert outbox[0].subject == 'Recipie App - Please Confirm Your Email Address'
        assert outbox[0].sender == 'flaskrecipieapp@gmail.com'
        assert outbox[0].recipients[0] == 'andrewflaskdev@gmail.com'
        # assert 'https://localhost:5000/users/confirm/' in outbox[0].html

def test_invalid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with invalid data (missing password)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/register',
                                data={'email': 'andrewflaskdev@gmail.com',
                                      'password_hashed': '',   # Empty field is not allowed!
                                      'username': 'andrewflaskdev',
                                      'first_name': 'Andrew',
                                      'last_name': 'Flaskdev'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, Andrew!' not in response.data
    assert b'Recipie' in response.data
    assert b'[This field is required.]' in response.data

def test_duplicate_email_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with the email address for an existing user
    THEN check an error message is returned to the user
    """
    test_client.post('/users/register',
                     data={'email': 'andrewflaskdev@gmail.com',
                           'password_hashed': 'password123',
                           'username': 'andrewflaskdev',
                           'first_name': 'Andrew',
                           'last_name': 'Flaskdev'},
                     follow_redirects=True)
    response = test_client.post('/users/register',
                                data={'email': 'andrewflaskdev@gmail.com',
                                      'password_hashed': 'password123',
                                      'username': 'andrewflaskdev',
                                      'first_name': 'Andrew',
                                      'last_name': 'Flaskdev'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, Andrew!' not in response.data
    assert b'Recipie' in response.data
    assert b'ERROR! Email (andrewflaskdev@gmail.com) already exists.' in response.data

###
def test_confirm_email_valid(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/confirm/<token>' page is requested (GET) with valid data
    THEN check that the user's email address is marked as confirmed
    """
    # Create the unique token for confirming a user's email address
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = confirm_serializer.dumps('andrewflaskdev@gmail.com', salt='email-confirmation-salt')

    response = test_client.get('/users/confirm/'+token, follow_redirects=True)
    assert response.status_code == 200
    assert b'Thank you for confirming your email address!' in response.data
    user = User.query.filter_by(email='andrewflaskdev@gmail.com').first()
    assert user.email_confirmed

def test_confirm_email_already_confirmed(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/confirm/<token>' page is requested (GET) with valid data
         but the user's email is already confirmed
    THEN check that the user's email address is marked as confirmed
    """
    # Create the unique token for confirming a user's email address
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = confirm_serializer.dumps('andrewflaskdev@gmail.com', salt='email-confirmation-salt')

    # Confirm the user's email address
    test_client.get('/users/confirm/'+token, follow_redirects=True)

    # Process a valid confirmation link for a user that has their email address already confirmed
    response = test_client.get('/users/confirm/'+token, follow_redirects=True)
    assert response.status_code == 200
    assert b'Account already confirmed.' in response.data
    user = User.query.filter_by(email='andrewflaskdev@gmail.com').first()
    assert user.email_confirmed

def test_confirm_email_invalid(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/confirm/<token>' page is is requested (GET) with invalid data
    THEN check that the link was not accepted
    """
    response = test_client.get('/users/confirm/bad_confirmation_link', follow_redirects=True)
    assert response.status_code == 200
    assert b'The confirmation link is invalid or has expired.' in response.data

def test_get_resend_email_confirmation_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing with the user logged in
    WHEN the '/users/resend_email_confirmation' page is retrieved (GET)
    THEN check that an email was queued up to send
    """
    with mail.record_messages() as outbox:
        response = test_client.get('/users/resend_email_confirmation', follow_redirects=True)
        assert response.status_code == 200
        assert b'Email sent to confirm your email address.  Please check your email!' in response.data
        assert len(outbox) == 1
        assert outbox[0].subject == 'Recipie App - Confirm Your Email Address'
        assert outbox[0].sender == 'flaskrecipieapp@gmail.com'
        assert outbox[0].recipients[0] == 'andrewflaskdev@gmail.com'
        assert 'http://localhost/users/confirm/' in outbox[0].html

def test_get_resend_email_confirmation_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing with the user not logged in
    WHEN the '/users/resend_email_confirmation' page is retrieved (GET)
    THEN check that an email was not queued up to send
    """
    with mail.record_messages() as outbox:
        response = test_client.get('/users/resend_email_confirmation', follow_redirects=True)
        assert response.status_code == 200
        assert b'Email sent to confirm your email address.  Please check your email!' not in response.data
        assert len(outbox) == 0
        assert b'Please log in to access this page.' in response.data        
