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
    assert b'Email: default_user@example.com' in response.data

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
    assert b'Email: default_user@example.com' not in response.data
    assert b'Please log in to access this page.' in response.data
