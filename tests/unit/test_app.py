"""
This file (test_app.py) contains the unit tests for the app.py file.
"""

def test_get_index(test_client):
    """
    GIVEN this Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Recipie' in response.data


        




        



 
