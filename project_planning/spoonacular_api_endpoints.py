import requests, json
from config import API_KEY

def send_cuisine_request():
    # Request
    # GET https://api.spoonacular.com/recipes/complexSearch

    """
    Returns a list of supported cuisines, including: 

    [African, American, British, Cajun, Caribbean, Chinese, Eastern
    European, European, French, German, Greek, Indian, Irish, Italian,
    Japanese, Jewish, Korean, Latin American, Mediterranean, Mexican,
    Middle Eastern, Nordic, Southern, Spanish, Thai, Vietnamese]
    """ 

    try:
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "cuisine": "Japanese",
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def send_diet_request():
    # Request
    # GET https://api.spoonacular.com/recipes/complexSearch

    """
    Returns a list of supported diets, including: 

    [Gluten Free, Ketogenic, Vegetarian, Lacto-Vegetarian, Ovo-Vegetarian,
    Vegan, Pescetarian, Paleo, Primal, Whole30]
    """    

    try:
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "diet": "Ketogenic"
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def send_type_request():
    # Request
    # GET https://api.spoonacular.com/recipes/complexSearch

    """
    Returns a list of supported diet types, including:

    [main course, side dish, dessert, appetizer, salad, bread, breakfast,
    soup, beverage, sauce, marinade, fingerfood, snack, drink]
    """

    try:
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "type": "drink"
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')        


def send_intolerances_request():
    # Request
    # GET https://api.spoonacular.com/recipes/complexSearch

    """
    Returns a list of supported intolerances, including:

    [Dairy, Egg, Gluten, Grain, Peanut, Seafood, Sesame, Shellfish, Soy,
    Sulfite, Tree Nut, Wheat]
    """

    try:
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "intolerances": "Dairy"
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

                
                
                
