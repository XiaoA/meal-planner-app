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
    THEN check the response is valid and the user is registered
    """
    response = test_client.post('/users/register',
                                data={'email': 'andrew@example.com',
                                      'password_hashed': 'Password123!',
                                      'password_confirmation_hashed': 'Password123!'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, andrew@example.com!' in response.data
    assert b'Recipie' in response.data
    assert len(outbox) == 1
    assert outbox[0].subject == 'Registration - Recipie App'
    assert outbox[0].sender == 'andrewflaskdev@gmail.com'
    assert outbox[0].recipients[0] == 'andrew@example.com'
    
def test_invalid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with invalid data (missing password)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/register',
                                data={'email': 'andrew2@example.com',
                                      'password_hashed': '',   # Empty field is not allowed!
                                      'password_confirmation_hashed': ''},   # Empty field is not allowed!
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
                     data={'email': 'alonzochurch@example.com',
                           'password_hashed': 'LambdaRules123!',
                           'password_confirmation_hashed': 'LambdaRules123!'},
                     follow_redirects=True)
    response = test_client.post('/users/register',
                                data={'email': 'alonzochurch@example.com',
                                      'password_hashed': 'LambdaRules123!',
                                      'password_confirmation_hashed': 'LambdaRules123!'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, Alonzo!' not in response.data
    assert b'Recipie' in response.data
    assert b'ERROR! Email (alonzochurch@example.com) already exists.' in response.data

