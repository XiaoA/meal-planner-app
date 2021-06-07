from . import users_blueprint
from flask import current_app, render_template
import requests
from project.models import User
from project import database

@users_blueprint.route('/users')
def list_users():
    users = User.query.order_by(User.id).all()
    return render_template('users/index.html', users=users)

