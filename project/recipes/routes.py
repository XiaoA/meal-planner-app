from . import recipes_blueprint
from flask import current_app, render_template, request, session, flash, redirect, url_for, jsonify, flash
import requests
from forms import SearchRecipesForm
from config import API_KEY, SECRET_KEY
from app import app

API_BASE_URL = "https://api.spoonacular.com"

# Request Callbacks
@recipes_blueprint.before_request
def stocks_before_request():
    current_app.logger.info('Calling before_request() for the stocks blueprint...')


@recipes_blueprint.after_request
def stocks_after_request(response):
    current_app.logger.info('Calling after_request() for the stocks blueprint...')
    return response


@recipes_blueprint.teardown_request
def stocks_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the stocks blueprint...')

# Recipe Blueprint Routes

@recipes_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = SearchRecipesForm()
    return render_template('recipes/index.html', form=form)

@recipes_blueprint.route('/recipes/search-results', methods=['GET', 'POST'])
def show_recipes():
    ingredient = request.form['query']
    response = requests.get(f"{API_BASE_URL}/food/ingredients/search", params={"apiKey": API_KEY, "query": ingredient})

    data = response.json()
    results = data['results']
    app.logger.info(f"Searched for recipes containing: { ingredient }")

    return render_template('/search-results.html', data=data)
