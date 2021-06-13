def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User object is created
    THEN add username (required), and password (required) to database
    """
    assert new_user.email == "andrewflaskdev@gmail.com"
    assert new_user.password_hashed != 'password123'

def test_set_password(new_user):
    """
    GIVEN a User model
    WHEN the user's password is changed
    THEN check the password has been changed
    """
    new_user.set_password('mynewpassword123')
    assert new_user.email == 'andrewflaskdev@gmail.com'
    assert new_user.is_password_correct('mynewpassword123')
