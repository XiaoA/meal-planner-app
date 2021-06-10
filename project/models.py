from project import database, bcrypt
from flask import current_app


class User(database.Model):
    """
    Class that handles user logins and authentication.

    The following attributes of a login are stored in this table:
        * user_id (as a foreign key. When a user successfully registers, the user_id is inserted into the logins table.)
        * email - the user's email
        * hashed password - hashed password (using Flask-Bcrypt)
        * password_confirmation_hashed - hashed password confirmation field
    """
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, unique=True)
    password_hashed = database.Column(database.String(264))
    password_confirmation_hashed = database.Column(database.String(264))
    user_profiles = database.relationship('UserProfile', backref='user', lazy='dynamic')

    def __init__(self, email: str, password_plaintext: str, password_confirmation_plaintext: str):
        self.email = email
        self.password_hashed = bcrypt.generate_password_hash(
            password_plaintext, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode('utf-8')
        self.password_confirmation_hashed = bcrypt.generate_password_hash(
            password_plaintext, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode('utf-8')



    def is_password_correct(self, password_plaintext: str):
        return bcrypt.check_password_hash(self.password_hashed, password_plaintext)

    def __repr__(self):
        return f'<User: {self.email} {self.password_hashed} {self.password_confirmation_hashed}>'

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)

class UserProfile(database.Model):
    """
    Class that represents a user's profile information.

    The following attributes of a user are stored in this table:
        username (type: string) 
        first_name (type: string) 
        last_name (type: string)

    The username attribute is required; first_name and last_name are optional.
    """

    __tablename__ = 'user_profiles'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    first_name = database.Column(database.String, nullable=True)
    last_name = database.Column(database.String, nullable=True)   
    user_id = database.Column(database.Integer, database.ForeignKey('users.id')) 

    def __init__(self, username: str, first_name: str, last_name: str, user_id: int):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
    
    def __repr__(self):
        """ Show info about user. """

        u = self
        return f"<UserProfile {u.username} {u.first_name} {u.last_name}"

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
