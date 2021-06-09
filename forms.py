from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from config import API_KEY

class SearchRecipesForm(FlaskForm):
    query = StringField("Recipe Search", validators=[InputRequired(message="Search term can't be blank.")])
    apiKey = API_KEY

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=30)])
    password_hashed = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=40)])
    password_confirmation_hashed = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=40)])
    submit = SubmitField('Register')
    
class NewUserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField('Last Name', validators=[Length(max=25)])    
    submit = SubmitField('Finish Registration')
