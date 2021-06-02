"""
This file (test_recipes.py) contains the functional tests for recipe searches and API calls.
"""
from app import app
from config import API_KEY

def test_show_recipes():
    """
    GIVEN this Flask application
    WHEN the '/search-results' page is posted to (POST)
    THEN check that the user is redirected to the '/search-results' page
    """
    with app.test_client() as client:
        response = client.post('/search-results', data={
            'query': 'beef',
            'apiKey': API_KEY
        })
        # Assert page loads successfully
        assert response.status_code == 200

        # Assert page title and API response data are displayed
        assert b'Search Results - Recipie' in response.data
        assert b'6008' in response.data
        assert b'beef broth' in response.data
        assert b'beef-broth.png' in response.data

        # Assert call to action (register account) is displayed
        assert b'Sign up!' in response.data
        assert b'Register for a free account to create search for more recipes, save them, and join our community!' in response.data
