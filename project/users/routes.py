from . import users_blueprint
from flask import current_app, render_template, flash, abort, request, redirect, url_for, session, copy_current_request_context, escape
import requests
from forms import RegistrationForm, LoginForm, EmailForm, PasswordForm, ChangePasswordForm
from project.models import User, UserProfile, Follows
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

@users_blueprint.route('/users', methods=['GET'])
@login_required
def show_all_users():
    # This should be refactored for better performance 
    users = User.query.order_by(User.id).all()
    user_profiles = UserProfile.query.order_by(UserProfile.id).all()
    return render_template('users/index.html', users=users, user_profiles=user_profiles)

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
                
                # return redirect(url_for('recipes.index))
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
        flash('Already logged in!')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('recipes.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password_hashed.data):
                user_id = user.id
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in, {current_user.email}!')
                current_app.logger.info(f'Logged in user: {current_user.email}')
                return redirect(url_for('users.show_user_profile', user_id=user_id))

        flash('ERROR! Incorrect login credentials.', 'danger')
    return render_template('users/login.html', form=form)

@users_blueprint.route('/users/logout')
@login_required
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('recipes.index'))

# @users_blueprint.route('/users/<int:user_profile_id>')
# @login_required
# def user_profile():
#     user_profile = UserProfile.query.get_or_404(user_profile_id).limit(10)
#     return render_template('users/profile.html', user_profile=user_profile)

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

@users_blueprint.route('/password_reset_via_email', methods=['GET', 'POST'])
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

@users_blueprint.route('/password_reset_via_token/<token>', methods=['GET', 'POST'])
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

@users_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.is_password_correct(form.current_password.data):
            current_user.set_password(form.new_password.data)
            database.session.add(current_user)
            database.session.commit()
            flash('Your password has been updated!', 'success')
            current_app.logger.info(f'Password updated for user: {current_user.email}')
            return redirect(url_for('users.user_profile'))
        else:
            flash('ERROR! Incorrect user credentials!')
            current_app.logger.info(f'Incorrect password change for user: {current_user.email}')
    return render_template('users/change_password.html', form=form)


@users_blueprint.route('/resend_email_confirmation')
def resend_email_confirmation():
    @copy_current_request_context
    def send_email(email_message):
        with current_app.app_context():
            mail.send(email_message)

    # Send an email to confirm the user's email address
    message = generate_confirmation_email(current_user.email)
    email_thread = Thread(target=send_email, args=[message])
    email_thread.start()

    flash('Email sent to confirm your email address.  Please check your email!', 'success')
    current_app.logger.info(f'Email re-sent to confirm email address for user: {current_user.email}')
    return redirect(url_for('users.user_profile'))

### Following

@users_blueprint.route('/users/<int:user_id>')
def show_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/profile.html', user=user)


@users_blueprint.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("users.login")

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)

@users_blueprint.route('/users/follow/<int:follow_id>', methods=['POST'])
def follow_user(follow_id):
    """Current user follows another user."""    

    if current_user.is_authenticated == False:
        flash("Access unauthorized.", "danger")
        return redirect("user.login")

    followed_user = User.query.get_or_404(follow_id)
    current_user.following.append(followed_user)
    database.session.commit()

    return redirect(f"/users/{current_user.id}/following")

@users_blueprint.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if current_user.is_authenticated == False:
    # if not current_user:
        flash("Access unauthorized.", "danger")
        return redirect("users.login")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@users_blueprint.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not current_user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    current_user.following.remove(followed_user)
    database.session.commit()

    return redirect(f"/users/{current_user.id}/following")
