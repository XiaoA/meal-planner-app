from . import recipes_blueprint
from flask import current_app, render_template, request, session, flash
from project import create_app
import requests
from forms import SearchRecipesForm
from config import API_BASE_URL, API_KEY

# Request Callbacks
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

# Recipe Blueprint Routes

@recipes_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = SearchRecipesForm()
    return render_template('recipes/index.html', form=form)

@recipes_blueprint.route('/recipes/search-results', methods=['GET', 'POST'])
def show_recipes():
    ingredient = request.form['query']
    response = requests.get(f"{API_BASE_URL}/food/ingredients/search", params={"apiKey": API_KEY, "query": ingredient})

    session['ingredient'] = ingredient
    data = response.json()
    results = data['results']
    
    current_app.logger.info(f"Searched for recipes containing: { ingredient }")

    flash(f"Searched for recipes with { ingredient }", 'success')    
    return render_template('/recipes/search-results.html', results=results)


