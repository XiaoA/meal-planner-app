from . import recipes_blueprint
from flask import current_app, render_template, request, session, flash
from project import create_app
from flask_login import current_user
import requests
from forms import SearchRecipesForm, SearchCuisineForm, SearchDietForm, SearchMealTypeForm, SearchIntoleranceTypeForm, ViewRecipeDetailsForm
from project.models import User, UserProfile
from config import API_BASE_URL, API_KEY

""" Request Callbacks """
@recipes_blueprint.before_request
def recipes_before_request():
    current_app.logger.info('Calling before_request() for the recipes blueprint...')


@recipes_blueprint.after_request
def recipes_after_request(response):
    current_app.logger.info('Calling after_request() for the recipes blueprint...')
    return response


@recipes_blueprint.teardown_request
def recipes_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the recipes blueprint...')

""" Recipe Index Routes """
@recipes_blueprint.route('/', methods=['GET', 'POST'])
# Ingredient Search
def index():
    form = SearchRecipesForm()
    return render_template('recipes/index.html', form=form)

# Cuisine Search
def search_cuisine_recipes():
    """
    Returns a list of supported cuisines, including: 

    [African, American, British, Cajun, Caribbean, Chinese, Eastern
    European, European, French, German, Greek, Indian, Irish, Italian,
    Japanese, Jewish, Korean, Latin American, Mediterranean, Mexican,
    Middle Eastern, Nordic, Southern, Spanish, Thai, Vietnamese]
    """
    search_cuisine_form = SearchCuisineForm()
    return render_template('recipes/index.html', form=search_cuisine_form)

# Diet Search
def search_diet_recipes():
    """
    Returns a list of supported specialty diets, including: 

    [Gluten Free, Ketogenic, Vegetarian, Lacto-Vegetarian, Ovo-Vegetarian,
    Vegan, Pescetarian, Paleo, Primal, Whole30]
    """
    search_diet_form = SearchDietForm()
    return render_template('recipes/index.html', form=search_diet_form)

# Meal Type Search
def search_meal_type_recipes():
    """
    Returns a list of supported specialty diets, including: 

    [Gluten Free, Ketogenic, Vegetarian, Lacto-Vegetarian, Ovo-Vegetarian,
    Vegan, Pescetarian, Paleo, Primal, Whole30]
    """
    search_meal_type_form = SearchMealTypeForm()
    return render_template('recipes/index.html', form=search_meal_type_form)

""" Show Search Results """
@recipes_blueprint.route('/recipes/search-results', methods=['GET', 'POST'])
# Show Ingredient Search Results
def show_recipes():
    ingredient = request.form['query']
    response = requests.get(f"{API_BASE_URL}/food/ingredients/search", params={"apiKey": API_KEY, "query": ingredient})

    session['ingredient'] = ingredient
    data = response.json()
    results = data['results']
    session['results'] = results

    current_app.logger.info(f"Searched for recipes containing: { ingredient }")

    flash(f"Searched for recipes with { ingredient }", 'success')    
    return render_template('/recipes/search-results.html', results=results)

def request_recipe_details():
    results = session['results']
    request_recipe_form = ViewRecipeDetailsForm()
    return render_template('recipes/search-results.html', form=request_recipe_form)

# Show Cusine Search Results
def show_cuisine_search_results():
    try:
        cuisine = request.form['query']
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "cuisine": cuisine
            }
        )
        session['cuisine'] = cuisine
        data = response.json()
        results = data['results']

        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        current_app.logger.info(f"Searched for { cuisine } recipes")

        flash(f"Searched for { cuisine } recipes", 'success')
        return render_template('recipes/search-results.html', results=results)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return render_template('recipes/index.html', form=search_cuisine_form)


# Show Diet Search Results 
def show_diet_recipe_results():
    diet = request.form['query']
    response = requests.get(f"{API_BASE_URL}", params={"apiKey": API_KEY, "query": diet})

    session['diet'] = diet
    data = response.json()
    results = data['results']

    current_app.logger.info(f"Searched for recipes containing: { diet }")

    flash(f"Searched for recipes with { diet }", 'success')    
    return render_template('/recipes/search-results.html', results=results)


@recipes_blueprint.route('/recipes/view-recipe-details', methods=['GET', 'POST'])
def view_recipe_details():
    try:
        response = requests.get(
            url=f"https://api.spoonacular.com/recipes/93772/information",
            params={
                "includeNutrition": "false",
                "apiKey": API_KEY,
            },
        )
        results = response.json()
        
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        return render_template('recipes/view-recipe-details.html', results=results)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return render_template('recipes/search-results.html')

    
