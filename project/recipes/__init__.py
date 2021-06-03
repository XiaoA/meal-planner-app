"""
The recipes blueprint allows for users to add, edit, and delete
recipe data from their portfolio.
"""
from flask import Blueprint

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

from . import routes
