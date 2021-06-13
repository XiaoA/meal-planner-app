from . import users_blueprint
from flask import current_app, render_template, flash, abort, request, redirect, url_for, session, copy_current_request_context, escape
import requests
from forms import RegistrationForm, LoginForm, EmailForm, PasswordForm
from project.models import User, UserProfile
from project import database, mail
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, login_required, logout_user
from urllib.parse import urlparse
from threading import Thread
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from datetime import datetime


""" Routes """

def generate_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    password_reset_url = url_for('users.process_password_reset_token',
                                 token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
                                 _external=True)

    return Message(subject='Recipie App - Password Reset Requested',
                   html=render_template('users/email_password_reset.html', password_reset_url=password_reset_url),
                   recipients=[user_email])

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
                new_user_registration = User(form.email.data, form.password_hashed.data)
                database.session.add(new_user_registration)
                database.session.commit()
                user_id = new_user_registration.id
                session['user_id'] = user_id

                user_id = session['user_id']
                new_user_profile = UserProfile(form.username.data, form.first_name.data, form.last_name.data, user_id)
                database.session.add(new_user_profile)
                database.session.commit()

                flash(f'Thanks for registering, {new_user_profile.username}! Please check your email to confirm your email address.', 'success')

                current_app.logger.info(f'Registered new user: {form.username.data}!')

                # Set app_context for email confirmation
                @copy_current_request_context
                def send_email(message):
                    with current_app.app_context():
                        mail.send(message)

                # Send an email confirming registration
                msg = generate_confirmation_email(form.email.data)
                email_thread = Thread(target=send_email, args=[msg])
                email_thread.start()
                
                # return redirect(url_for('recipes.index'))
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

def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('users.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                          _external=True)

    return Message(subject='Recipie App - Please Confirm Your Email Address',
                   html=render_template('users/email-confirmation.html', confirm_url=confirm_url),
                   recipients=[user_email])

@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except BadSignature as e:
        flash(f'The confirmation link is invalid or has expired.', 'error')
        current_app.logger.info(f'Invalid or expired confirmation link received from IP address: {request.remote_addr}')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
        current_app.logger.info(f'Confirmation link received for a confirmed user: {user.email}')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        database.session.add(user)
        database.session.commit()
        flash('Thank you for confirming your email address!', 'success')
        current_app.logger.info(f'Email address confirmed for: {user.email}')

    return redirect(url_for('recipes.index'))

@users_blueprint.route('/password_reset_via_email', methods=['GET', 'POST'])
def password_reset_via_email():
    form = EmailForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Error! Invalid email address!', 'error')
            return render_template('users/password_reset_via_email.html', form=form)

        if user.email_confirmed:
            @copy_current_request_context
            def send_email(email_message):
                with current_app.app_context():
                    mail.send(email_message)

            # Send an email confirming the new registration
            message = generate_password_reset_email(form.email.data)
            email_thread = Thread(target=send_email, args=[message])
            email_thread.start()

            flash('Please check your email for a password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('users.login'))

    return render_template('users/password_reset_via_email.html', form=form)

@users_blueprint.route('/password_reset_via_token/<token>', methods=['GET', 'POST'])
def process_password_reset_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except BadSignature as e:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))

        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/reset_password_with_token.html', form=form)
