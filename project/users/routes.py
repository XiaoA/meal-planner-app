from . import users_blueprint
from flask import current_app, render_template, flash, abort, request, redirect, url_for, session, copy_current_request_context
import requests
from forms import RegistrationForm, LoginForm
from project.models import User, UserProfile
from project import database
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, login_required, logout_user
from threading import Thread

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

                user_id = session['user_id']
                new_user_profile = UserProfile(form.username.data, form.first_name.data, form.last_name.data, user_id)
                database.session.add(new_user_profile)
                database.session.commit()

                flash(f'Thanks for registering, {new_user_profile.username}!')
                current_app.logger.info(f'Registered new user: {form.username.data}!')
                return redirect(url_for('recipes.index'))

                # Send an email confirming registration
                msg = Message(subject='Registration - Recipie App',
                              body='Thanks for registering with Recipie!',
                              recipients=[form.email.data])
                mail.send(msg)
                return redirect(url_for('users.login'))
            
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! Email ({form.email.data}) already exists.', 'error')
        else:
            flash(f"Error in form data!", 'error')
            
    return render_template('users/register.html', form=form)

@users_blueprint.route('/users/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('recipes.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password_hashed.data):
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in, {current_user.email}!')
                current_app.logger.info(f'Logged in user: {current_user.email}')
                return redirect(url_for('recipes.index'))

        flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/users/logout')
@login_required
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('recipes.index'))

@users_blueprint.route('/users/profile')
@login_required
def user_profile():
    return render_template('users/profile.html')

