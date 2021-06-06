def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User object is created
    THEN add username (required), first name (required), and last name (optional) to database
    """
    assert new_user.username == "batman99"
    assert new_user.first_name == "Bruce"
    assert new_user.last_name == "Wayne"
