from . import recipes_blueprint
from flask import current_app, render_template, request, session, flash, redirect, url_for, json
from project import create_app, database
from flask_login import current_user, login_required
import requests
from forms import SearchIngredientForm, SearchCuisineForm, SearchDietForm, SearchMealTypeForm, SearchIntoleranceTypeForm, ViewRecipeDetailsForm, LoginForm
from project.models import User, UserProfile, RecipeBox, Meal
from config import API_BASE_URL, API_KEY
from sqlalchemy.exc import IntegrityError

""" Recipe Index Routes """
@recipes_blueprint.route('/', methods=['GET'])
# Ingredient Search
def index():
    search_ingredient_form = SearchIngredientForm()
    return render_template('recipes/index.html', form=search_ingredient_form)

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

    return render_template('recipes/index.html', form=search_cuisine_form, choices=choices)

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


# Show Ingredient Search Results
@recipes_blueprint.route('/recipes/search-results', methods=['GET'])
def show_ingredient_search_results():
    try:
        ingredient = request.args['query']
        response = requests.get(
            f"{API_BASE_URL}/food/ingredients/search",
            params={
                "apiKey": API_KEY,
                "query": ingredient,
                "number": "4"
            }
        )
        results = response.json()['results']
        current_app.logger.info(f"Searched for recipes containing: { ingredient }")
        flash(f"Searched for recipes with { ingredient }", 'success')    

        return render_template('recipes/search-results.html', results=results)
    except requests.exceptions.RequestException:
        flash('Your search failed', 'danger')
        return render_template('recipes/index.html')
    
# Show Cuisine Search Results
def show_cuisine_search_results():
    try:
        cuisine = request.args['query']
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "query": cuisine,
                "number": "4",
            }
        )
        
        results = response.json()['results']
        import ipdb; ipdb.set_trace()
        return render_template('recipes/search-results.html', results=results)
    # current_app.logger.info(f"Searched for { cuisine }")
    # flash(f"Searched for { cuisine }", 'success')
    except requests.exceptions.RequestException:
        flash('Your search failed', 'danger')
        return render_template('recipes/index.html')

# Show Diet Search Results 
def show_diet_search_results():
    try:
        diet = request.args['query']
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "query": diet,
                "number": "4",
            }
        )
        results = response.json()['results']
        current_app.logger.info(f"Searched for { diet } recipes")
        flash(f"Searched for { diet }", 'success')    
        return render_template('recipes/search-results.html', results=results)
    except requests.exceptions.RequestException:
        flash('Your search failed', 'danger')
        return render_template('recipes/index.html')

# Show Meal Type Search Results 
def show_meal_type_search_results():
    try:
        meal_type = request.args['query']
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "query": meal_type,
                "number": "4",
            }
        )
        results = response.json()['results']
        current_app.logger.info(f"Searched for { meal_type }")
        flash(f"Searched for { meal_type }", 'success')    
        return render_template('recipes/search-results.html', results=results)
    except requests.exceptions.RequestException:
        flash('Your search failed', 'danger')
        return render_template('recipes/index.html')    

# Show Dietary Intolerance Search Results
def show_dietary_intolerance_search_results():
    try:
        intolerance = request.args['query']
        response = requests.get(
            url="https://api.spoonacular.com/recipes/complexSearch",
            params={
                "apiKey": API_KEY,
                "query": intolerance,
            }
        )
        results = response.json()['results']
        current_app.logger.info(f"Searched for { intolerance }")
        flash(f"Searched for { intolerance }", 'success')    
        return render_template('recipes/search-results.html', results=results)
    except requests.exceptions.RequestException:
        flash('Your search failed', 'danger')
        return render_template('recipes/index.html')

# View Recipe Details
@recipes_blueprint.route('/recipes/view-recipe-details/<int:recipe_id>', methods=['GET', 'POST'])
def view_recipe_details(recipe_id):
    try:
        response = requests.get(
            url=f"https://api.spoonacular.com/recipes/{recipe_id}/information",
            params={
                "includeNutrition": "false",
                "apiKey": API_KEY,
            },
        )
        results = response.json()
        recipe_id = response.json()['id']
        recipe_url = response.json()['sourceUrl']
        # import ipdb; ipdb.set_trace()

        return render_template('recipes/view-recipe-details.html', results=results, recipe_id=recipe_id)
    except requests.exceptions.RequestException:
        flash('Your search failed', 'danger')
        return render_template('recipes/index.html')

# Like Recipes    
@recipes_blueprint.route('/recipes/like-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def like_recipe(recipe_id):
    recipe_id = recipe_id
    if request.method == 'POST':
        if current_user.is_authenticated:
            try:
                is_liked = True
                recipe_url = request.form['recipe_url']
                user_id = current_user.id

                new_like_recipe = RecipeBox(is_liked, recipe_url, user_id)
                database.session.add(new_like_recipe)
                database.session.commit()
                flash("You liked this recipe", "success")
                return redirect(url_for('recipes.view_recipe_details', recipe_id=recipe_id))
            except IntegrityError:
                database.session.rollback()
                flash(f"You've already liked this recipe!", "danger")
                return redirect(url_for('recipes.view_recipe_details', recipe_id=recipe_id))

            

# Add New Meal
@recipes_blueprint.route('/recipes/add-new-meal/<int:recipe_id>', methods=['GET', 'POST'])
@login_required            
def add_new_meal(recipe_id):
    recipe_id = recipe_id
    if request.method == 'POST':
        if current_user.is_authenticated:
            try:
                meal_date = request.form['meal_date']
                meal_title = request.form['meal_title']
                meal_notes = request.form['meal_notes']
                recipe_id = request.form['recipe_id']
                recipe_title = request.form['recipe_title']
                recipe_url = request.form['recipe_url']
                user_id = current_user.id                

                new_meal_plan = Meal(meal_date, meal_title, meal_notes, recipe_id, recipe_title, recipe_url, user_id)
                database.session.add(new_meal_plan)
                database.session.commit()
                flash("You created a new meal plan", "success")
                return redirect(url_for('recipes.view_recipe_details', recipe_id=recipe_id))
            except IntegrityError:
                database.session.rollback()
                flash(f"You've already saved this recipe!", "danger")
                return redirect(url_for('recipes.view_recipe_details', recipe_id=recipe_id))

@recipes_blueprint.route('/recipes/recipe-box', methods=['GET'])
def show_recipe_box():
    return render_template('recipes/recipe-box.html')


