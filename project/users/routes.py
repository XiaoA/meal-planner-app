from . import users_blueprint
from flask import current_app, render_template, flash, abort, request, redirect, url_for, session, copy_current_request_context, escape, jsonify
import requests
from forms import RegistrationForm, LoginForm, EmailForm, PasswordForm, ChangePasswordForm, FollowingForm
from project.models import User, UserProfile, RecipeBox, Meal
from project import database, mail
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, login_required, logout_user
from urllib.parse import urlparse
from threading import Thread
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from datetime import datetime

""" Error Handlers """
@users_blueprint.errorhandler(403)
def page_forbidden(e):
    return render_template('users/403.html'), 403

""" Helpers """

def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('users.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                          _external=True)

    return Message(subject='Recipie App - Please Confirm Your Email Address',
                   html=render_template('users/email_confirmation.html', confirm_url=confirm_url),
                   recipients=[user_email])

def generate_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    password_reset_url = url_for('users.process_password_reset_token',
                                 token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
                                 _external=True)

    return Message(subject='Recipie App - Password Reset Requested',
                   html=render_template('users/email_password_reset.html', password_reset_url=password_reset_url),
                   recipients=[user_email])

@users_blueprint.route('/users', methods=['GET'])
@login_required
def show_all_users():
    # This should be refactored for better performance 
    user_profiles = UserProfile.query.order_by(UserProfile.id).all()
    return render_template('users/index.html', user_profiles=user_profiles)

""" Routes """



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

                return redirect(url_for('users.login'))
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! Email ({form.email.data}) already exists.', 'danger')
        else:
            flash(f"Error in form data!", 'danger')
            
    return render_template('users/register.html', form=form)

@users_blueprint.route('/users/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!', 'danger')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('recipes.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            user_profile = user.user_profiles.first()
            if user and user.is_password_correct(form.password_hashed.data):

                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in, {current_user.email}!', 'success')
                current_app.logger.info(f'Logged in user: {current_user.email}')
                
                return render_template('users/profile.html', user=user, user_profile=user_profile)

        flash('ERROR! Incorrect login credentials.', 'danger')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/users/logout')
@login_required
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Goodbye!', 'primary')
    return redirect(url_for('recipes.index'))

@users_blueprint.route('/users/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except BadSignature as e:
        flash(f'The confirmation link is invalid or has expired.', 'danger')
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

@users_blueprint.route('/users/password_reset_via_email', methods=['GET', 'POST'])
def password_reset_via_email():
    form = EmailForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Error! Invalid email address!', 'danger')
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
            flash('Your email address must be confirmed before attempting a password reset.', 'danger')
        return redirect(url_for('users.login'))

    return render_template('users/password_reset_via_email.html', form=form)

@users_blueprint.route('/users/password_reset_via_token/<token>', methods=['GET', 'POST'])
def process_password_reset_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except BadSignature as e:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('Invalid email address!', 'danger')
            return redirect(url_for('users.login'))

        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/reset_password_with_token.html', form=form)

@users_blueprint.route('/users/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.is_password_correct(form.current_password.data):
            current_user.set_password(form.new_password.data)
            user_id = current_user.id

            database.session.add(current_user)
            database.session.commit()
            flash('Your password has been updated!', 'success')
            current_app.logger.info(f'Password updated for user: {current_user.email}')
            return redirect(url_for('users.show_user_profile', user_id=user_id))
        else:
            flash('ERROR! Incorrect user credentials!', 'danger')
            current_app.logger.info(f'Incorrect password change for user: {current_user.email}')
    return render_template('users/change_password.html', form=form)


@users_blueprint.route('/users/resend_email_confirmation')
@login_required
def resend_email_confirmation():
    @copy_current_request_context
    def send_email(email_message):
        with current_app.app_context():
            mail.send(email_message)

    # Send an email to confirm the user's email address
    message = generate_confirmation_email(current_user.email)
    email_thread = Thread(target=send_email, args=[message])
    email_thread.start()

    user_id = current_user.id
    flash('Email sent to confirm your email address.  Please check your email!', 'success')
    current_app.logger.info(f'Email re-sent to confirm email address for user: {current_user.email}')
    return redirect(url_for('users.show_user_profile', user_id=user_id))

""" Following """
@users_blueprint.route('/users/<int:user_id>')
@login_required
def show_user_profile(user_id):
    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("users.login")
    form = FollowingForm()
    user = User.query.get_or_404(user_id)
    user_profile = user.user_profiles.first()
    return render_template('users/profile.html', user=user, user_profile=user_profile, form=form)

@users_blueprint.route('/users/<int:user_id>/following')
@login_required
def show_following(user_id):
    """Show list of people this user is following."""

    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("users.login")

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)

@users_blueprint.route('/users/follow/<int:user_id>', methods=['GET','POST'])
@login_required
def follow_user(user_id):
    """Current user follows another user."""
    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("user.login")
    
    form = FollowingForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        user_profile = user.user_profiles.first()
        if user is None:
            flash('User {} not found.'.format(user))
            return redirect(url_for('users'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('users.show_all_users', user=user))
        current_user.follow(user)
        database.session.commit()
        flash(f'You are following {user_profile.username}.', 'success')
        return redirect(url_for('users.show_all_users', user=user))
    else:
        return redirect(url_for('users'))

@users_blueprint.route('/users/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow_user(user_id):
    """Have currently-logged-in-user stop following this user."""

    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = FollowingForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        user_profile = user.user_profiles.first()
        if user is None:
            flash(f'User {user} not found.')
            return redirect(url_for('users'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('users.show_all_users', user=user))
        current_user.unfollow(user)
        database.session.commit()
        flash(f'You are not following {user_profile.username}.', 'success')
        return redirect(url_for('users.show_all_users', user=user))
    else:
        return redirect(url_for('users'))

@users_blueprint.route('/users/<int:user_id>/followers')
@login_required
def users_followers(user_id):
    """Show list of followers of this user."""

    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("users.login")

    user = User.query.get_or_404(user_id)
    
    return render_template('users/followers.html', user=user)

@users_blueprint.route('/users/<int:user_id>/recipes', methods=['GET'])
@login_required
def show_recipe_box(user_id):
    """Show an authenticated user's saved recipes."""
    user = User.query.get_or_404(user_id)
    user_profile = user.user_profiles.first()
    user_recipes = user.user_recipes.all()
    return render_template("users/recipes.html", user_id=user_id, user_profile=user_profile, user_recipes=user_recipes)

@users_blueprint.route('/users/<int:user_id>/meal-plans', methods=['GET'])
@login_required
def show_meal_plans(user_id):
    """Show an authenticated user's meal plans."""
def show_meal_plans(user_id):
    """Show an authenticated user's meal plans."""
    user_id = current_user.id
    if not current_user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    meal_plans = Meal.query.filter(user_id == current_user.id)
    return render_template("users/meal-plans.html", user_id=user_id, meal_plans=meal_plans)

