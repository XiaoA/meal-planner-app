"""
This file (test_recipes.py) contains the functional tests for recipe searches and API calls.
"""
from config import API_KEY
import requests
import json

""" Helpers """
class MockSuccessResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.headers = {'key': 'val'}

    def json(self):
        return {
            "results": {
                 "id": '652078',
                 "title": "Miso Soup With Thin Noodles",
                 "image": "https://spoonacular.com/recipeImages/652078-312x231.jpg",
                }
            }

    

class MockFailedResponse(object):
    def __init__(self, url):
        self.status_code = 404
        self.url = url
        self.headers = {'blaa': '1234'}

    def json(self):
        return {'error': 'bad'}   

""" Recipe Tests """

def test_cuisine_search_monkeypatch_get_success(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockSuccessResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&cuisine=Japanese'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    assert request.status_code == 200
    assert request.url == url
    assert '652078' in request.json()['results']['id']
    assert 'Miso Soup With Thin Noodles' in request.json()['results']['title']
    assert "https://spoonacular.com/recipeImages/652078-312x231.jpg" in request.json()['results']["image"]

def test_cuisine_searchmonkeypatch_get_failure(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockFailedResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&cuisine=Japanese'
    monkeypatch.setattr(requests, 'get', mock_get)
    r = requests.get(url)
    print(r.json())
    assert r.status_code == 404
    assert r.url == url
    assert 'bad' in r.json()['error']    

# def test_show_recipes(test_client):
#                 """
#     GIVEN this Flask application
#     WHEN the '/search-results' page is posted to (POST)
#     THEN check that the user is redirected to the '/search-results' page
#     """

#     response = test_client.post('/recipes/search-results', data={
#         'query': 'beef',
#         'apiKey': API_KEY
#     })
#                 # Assert page loads successfully
#     assert response.status_code == 200
                
#     # Assert page title and API response data are displayed
#     assert b'Search Results - Recipie' in response.data
#                 assert b'6008' in response.data
#                 assert b'https://spoonacular.com/recipeImages/6008-556x370.jpg' in response.data
