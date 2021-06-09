def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User object is created
    THEN add username (required), and password (required) to database
    """
    assert new_user.email == "batman@example.com"
    assert new_user.password_hashed != 'password'
    assert new_user.password_confirmation_hashed != 'password'
