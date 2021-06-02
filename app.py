from flask import Flask, render_template, request, jsonify, redirect, flash, json, session
import requests
from forms import SearchRecipesForm
from config import API_KEY, SECRET_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'
API_BASE_URL = "https://api.spoonacular.com"

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

    return render_template('search-results.html', data=data)

