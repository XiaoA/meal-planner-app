from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from config import API_KEY

""" Recipe Search Forms"""
class SearchIngredientForm(FlaskForm):
    query = StringField("Recipe Search", validators=[InputRequired(message="Search term can't be blank.")], render_kw={"placeholder": "chicken"})
    apiKey = API_KEY

class SearchCuisineForm(FlaskForm):
    choices=[
        'African', 'American', 'British', 'Cajun',
        'Caribbean', 'Chinese', 'Eastern European',
        'European', 'French', 'German', 'Greek', 'Indian',
        'Irish', 'Italian', 'Japanese', 'Jewish', 'Korean',
        'Latin American', 'Mediterranean', 'Mexican',
        'Middle Eastern', 'Nordic', 'Southern', 'Spanish',
        'Thai', 'Vietnamese']
    query = SelectField("Search by Cuisine", choices=[(cu, cu) for cu in choices])
    apiKey = API_KEY

class SearchDietForm(FlaskForm):
    diet = SelectField("Search by Diet", choices=[
        ('Gluten Free'), ('Ketogenic'), ('Vegetarian'), ('Lacto-Vegetarian'),
        ('Ovo-Vegetarian'), ('Vegan'), ('Pescetarian'), ('Paleo'), ('Primal'), ('Whole30')])
    apiKey = API_KEY

class SearchMealTypeForm(FlaskForm):
    type = SelectField("Search by Meal Type", choices=[
        ('main course'), ('side dish'), ('dessert'), ('appetizer'),
        ('salad'), ('bread'), ('breakfast'), ('soup'), ('beverage'),
        ('sauce'), ('marinade'), ('fingerfood'), ('snack'), ('drink')])
    apiKey = API_KEY

class SearchIntoleranceTypeForm(FlaskForm):
    type = SelectField("Search by Dietary Intolerance", choices=[
        ('Dairy'), ('Egg'), ('Gluten'), ('Grain'), ('Peanut'), ('Seafood'),
        ('Sesame'), ('Shellfish'), ('Soy'), ('Sulfite'), ('Tree Nut'), ('Wheat')])
    apiKey = API_KEY

class ViewRecipeDetailsForm(FlaskForm):
    apiKey = API_KEY

""" User Forms """    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=30)])
    password_hashed = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=40)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField('Last Name', validators=[Length(max=25)])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    password_hashed = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    submit = SubmitField('Submit')
    
class PasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')    

class FollowingForm(FlaskForm):
    submit = SubmitField('Submit')
