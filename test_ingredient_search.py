from app import app
from config import API_KEY

def test_get_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_show_recipes():
    with app.test_client() as client:
        response = client.post('/search-results', data={
            'query': 'beef',
            'apiKey': API_KEY
        })
        assert response.status_code == 200
        assert b'Search Results - Recipie' in response.data

        
        assert b'6008' in response.data
        assert b'beef broth' in response.data
        assert b'beef-broth.png' in response.data



        



 
