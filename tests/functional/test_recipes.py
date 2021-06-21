"""
This file (test_recipes.py) contains the functional tests for recipe searches and API calls.
"""
from config import API_KEY
import requests
import json

""" Helpers """
# Failing Search Test
""" Shared by all search types """
class MockFailedResponse(object):
    def __init__(self, url):
        self.status_code = 404
        self.url = url
        self.headers = {'key': 'value'}

    def json(self):
        return {'error': 'bad'}  

    
# Successful Cuisine Search
class MockCuisineSuccessResponse(object):
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
    
# Successful Diet Search
class MockDietSuccessResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.headers = {'key': 'val'}

    def json(self):
        return {
            "results": {
                "id": '646512',
                "title": "Salmon Caesar Salad",
                "image": "https://spoonacular.com/recipeImages/646512-312x231.jpg",
            }
        }

# Successful Meal Type Search
class MockMealTypeSuccessResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.headers = {'key': 'val'}

    def json(self):
        return {
            "results": {
                "id": '663845',
                "title": "TROPICAL BANANA GREEN SMOOTHIE",
                "image": "https://spoonacular.com/recipeImages/663845-312x231.jpg",
            }
        }    

# Successful Dietary Intolerance Search
class MockIntoleranceSuccessResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.headers = {'key': 'val'}

    def json(self):
        return {
            "results": {
                "id": "716268",
                "title": "African Chicken Peanut Stew",
                "image": "https://spoonacular.com/recipeImages/716268-312x231.jpg",
            }
        }    

""" Recipe Tests """
# Cuisine Searches
def test_cuisine_search_monkeypatch_get_success(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockCuisineSuccessResponse(url)

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
    request = requests.get(url)
    print(request.json())
    assert request.status_code == 404
    assert request.url == url
    assert 'bad' in request.json()['error']

# Diet Searches
def test_diet_search_monkeypatch_get_success(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockDietSuccessResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&diet=Ketogenic'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    assert request.status_code == 200
    assert request.url == url
    assert 'diet=Ketogenic' in request.url
    assert '646512' in request.json()['results']['id']
    assert 'Salmon Caesar Salad' in request.json()['results']['title']
    assert "https://spoonacular.com/recipeImages/646512-312x231.jpg" in request.json()['results']["image"]

def test_diet_searchmonkeypatch_get_failure(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockFailedResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&diet=Ketogenic'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    print(request.json())
    assert request.status_code == 404
    assert request.url == url
    assert 'bad' in request.json()['error']    

# Meal Type Searches
def test_meal_type_search_monkeypatch_get_success(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockMealTypeSuccessResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&type=drink'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    assert request.status_code == 200
    assert request.url == url
    assert 'type=drink' in request.url
    assert '663845' in request.json()['results']['id']
    assert 'TROPICAL BANANA GREEN SMOOTHIE' in request.json()['results']['title']
    assert "https://spoonacular.com/recipeImages/663845-312x231.jpg" in request.json()['results']["image"]

def test_diet_search_monkeypatch_get_failure(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockFailedResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&diet=Ketogenic'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    print(request.json())
    assert request.status_code == 404
    assert request.url == url
    assert 'bad' in request.json()['error']    

# Dietary Intolerance Searches
def test_intolerance_search_monkeypatch_get_success(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockIntoleranceSuccessResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&intolerances=Dairy'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    assert request.status_code == 200
    assert request.url == url
    assert 'intolerances=Dairy' in request.url
    assert '716268' in request.json()['results']['id']
    assert 'African Chicken Peanut Stew' in request.json()['results']['title']
    assert "https://spoonacular.com/recipeImages/716268-312x231.jpg" in request.json()['results']["image"]

def test_intolerance_search_monkeypatch_get_failure(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockFailedResponse(url)

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&intolerances=Dairy'
    monkeypatch.setattr(requests, 'get', mock_get)
    request = requests.get(url)
    print(request.json())
    assert request.status_code == 404
    assert request.url == url
    assert 'bad' in request.json()['error']    

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

