from . import recipes_blueprint
from flask import current_app, render_template, request, session, flash, redirect, url_for
import requests
from forms import SearchRecipesForm
from config import API_KEY
from app import app

API_BASE_URL = "https://api.spoonacular.com"

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
