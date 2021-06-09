from . import users_blueprint
from flask import current_app, render_template, flash, abort, request, redirect, url_for, session
import requests
from forms import RegistrationForm, NewUserProfileForm
from project.models import User, UserProfile
from project import database
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

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
                new_user_registration = User(form.email.data, form.password_hashed.data, form.password_confirmation_hashed.data)
                database.session.add(new_user_registration)
                database.session.commit()
                user_id = new_user_registration.id
                session['user_id'] = user_id
                                             

                current_app.logger.info(f'Registered new user: {form.email.data}!')
                return redirect(url_for('users.new_user_profile'))
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! Email ({form.email.data}) already exists.', 'error')
        else:
            flash(f"Error in form data!", 'error')
            
    return render_template('users/register.html', form=form)

@users_blueprint.route('/users/new', methods=['GET', 'POST'])
def new_user_profile():
    form = NewUserProfileForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_id = session['user_id']
                new_user_profile = UserProfile(form.username.data, form.first_name.data, form.last_name.data, user_id)
                database.session.add(new_user_profile)
                database.session.commit()

                flash(f'Thanks for registering, {new_user_profile.username}!')
                current_app.logger.info(f'Registered new user: {form.username.data}!')
                return redirect(url_for('recipes.index'))
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! User ({form.username.data}) already exists.', 'error')
        else:
            flash(f"Error in form data!", 'error')
            
    return render_template('users/new.html', form=form)

