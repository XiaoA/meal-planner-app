from . import users_blueprint
from flask import current_app, render_template, flash, abort, request, redirect, url_for
import requests
from forms import RegistrationForm
from project.models import User, Login
from project import database
from sqlalchemy.exc import IntegrityError

@users_blueprint.route('/users')
def list_users():
    users = User.query.order_by(User.id).all()
    return render_template('users/index.html', users=users)

@users_blueprint.route('/users/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_registration = Login(form.email.data, form.password_hashed.data, form.password_confirmation_hashed.data)
                database.session.add(new_registration)
                database.session.commit()

                flash(f'Thanks for registering, {new_registration.email}!')
                current_app.logger.info(f'Registered new user: {form.email.data}!')
                return redirect(url_for('recipes.index'))
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! Email ({form.email.data}) already exists.', 'error')
        else:
            flash(f"Error in form data!", 'error')
            
    return render_template('users/register.html', form=form)
