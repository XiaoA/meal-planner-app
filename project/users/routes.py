from . import users_blueprint

from flask import current_app, render_template, request, session, flash, redirect, url_for


@users_blueprint.route('/users')
def users_list():
    return "User List"
