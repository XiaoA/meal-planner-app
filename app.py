from flask import Flask, render_template, request, jsonify, redirect, flash, json, session
import requests
from forms import SearchRecipesForm
from config import API_KEY, SECRET_KEY
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'
API_BASE_URL = "https://api.spoonacular.com"

# Remove the default Flask logger
app.logger.removeHandler(default_handler)

# Configure custom logging
file_handler = RotatingFileHandler('instance/recipie.log',
                                   maxBytes=16384,
                                   backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Log application startup event
app.logger.info('Starting Recipie App...')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchRecipesForm()
    return render_template('index.html', form=form)

@app.route('/search-results', methods=['GET', 'POST'])
def show_recipes():
    ingredient = request.form['query']
    response = requests.get(f"{API_BASE_URL}/food/ingredients/search", params={"apiKey": API_KEY, "query": ingredient})

    data = response.json()
    results = data['results']
    app.logger.info(f"Searched for recipes containing: { ingredient }")

    return render_template('search-results.html', data=data)

