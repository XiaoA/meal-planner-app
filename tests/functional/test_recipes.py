"""
This file (test_recipes.py) contains the functional tests for recipe searches and API calls.
"""
# from config import API_KEY

# def test_show_recipes(test_client):
#     """
#     GIVEN this Flask application
#     WHEN the '/search-results' page is posted to (POST)
#     THEN check that the user is redirected to the '/search-results' page
#     """

#     response = test_client.post('/recipes/search-results', data={
#         'query': 'beef',
#         'apiKey': API_KEY
#     })
#     # Assert page loads successfully
#     assert response.status_code == 200
    
#     # Assert page title and API response data are displayed
#     assert b'Search Results - Recipie' in response.data
#     assert b'6008' in response.data
#     assert b'https://spoonacular.com/recipeImages/6008-556x370.jpg' in response.data
