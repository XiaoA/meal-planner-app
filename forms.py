from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from config import API_KEY

class SearchRecipesForm(FlaskForm):
    query = StringField("Recipe Search", validators=[InputRequired(message="Search term can't be blank.")])
    apiKey = API_KEY

class SearchCuisineForm(FlaskForm):
    cuisine = SelectField("Search by Cuisine", choices=[
        ('African'), ('American'), ('British'), ('Cajun'),
        ('Caribbean'), ('Chinese'), ('Eastern European'),
        ('European'), ('French'), ('German'), ('Greek'), ('Indian'),
        ('Irish'), ('Italian'), ('Japanese'), ('Jewish'), ('Korean'),
        ('Latin American'), ('Mediterranean'), ('Mexican'),
        ('Middle Eastern'), ('Nordic'), ('Southern'), ('Spanish'),
        ('Thai'), ('Vietnamese')])
    apiKey = API_KEY

class SearchDietForm(FlaskForm):
    diet = SelectField("Search by Diet", choices=[
        ('Gluten Free'), ('Ketogenic'), ('Vegetarian'), ('Lacto-Vegetarian'),
        ('Ovo-Vegetarian'), ('Vegan'), ('Pescetarian'), ('Paleo'), ('Primal'), ('Whole30')])
    apiKey = API_KEY    

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
    password = PasswordField('New Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password: ', validators=[DataRequired()])
    new_password = PasswordField('New Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
