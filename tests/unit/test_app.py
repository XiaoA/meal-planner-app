""" This file (test_app.py) contains the unit tests for the app.py file. """

def test_index_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_get_index(test_client):
    """
    GIVEN this Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Recipie' in response.data
    assert b'Finding new recipies is as easy as Reci<span class="pie-text">pie</span>!' in response.data
    assert b'A recipe has no soul. You as the cook must bring soul to the recipe' in response.data
    assert b"Here's what's cooking..." in response.data
    assert b'Search for new recipes.' in response.data
    assert b'Save your favorites. Plan your next meal!' in response.data
    assert b'Copycats welcome.' in response.data
    assert b'Try a random ingredient search...' in response.data
    assert b'Or, try a custom search!' in response.data
    assert b'Search by Cuisine' in response.data
    assert b'Search by Diet Type' in response.data
    assert b'Search by Meal Type' in response.data
    assert b'Search by Dietary Intolerance' in response.data

        




        



 
