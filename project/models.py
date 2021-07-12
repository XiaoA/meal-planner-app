from project import database, bcrypt
from flask import current_app
from datetime import datetime


followers = database.Table('followers',
    database.Column('follower_id', database.Integer, database.ForeignKey('users.id')),
    database.Column('followed_id', database.Integer, database.ForeignKey('users.id'))
)

class User(database.Model):
    """
    Class that handles user logins and authentication.

    The following attributes of a login are stored in this table:
        * user_id (as a foreign key. When a user successfully registers, the user_id is inserted into the logins table.)
        * email - the user's email
        * hashed password - hashed password (using Flask-Bcrypt)
        * A foreign key relationship with UserProfile, which joins data from the Users and UserProfiles tables
        * A foreign key relationship with Follow, which manages a self-referential follower/following relatitionship.
    """
    __tablename__ = 'users'

    id = database.Column(
        database.Integer,
        primary_key=True
    )
    
    email = database.Column(
        database.String,
        unique=True,
        nullable=False
    )
    
    password_hashed = database.Column(
        database.String(264),
        nullable=False
    )
    
    registered_on = database.Column(
        database.DateTime,
        nullable=True
    )
    
    email_confirmation_sent_on = database.Column(
        database.DateTime,
        nullable=True
    )
    
    email_confirmed = database.Column(
        database.Boolean,
        default=False
    )
    
    email_confirmed_on = database.Column(
        database.DateTime,
        nullable=True
    )             

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None

    user_profiles = database.relationship(
        'UserProfile',
        backref='user',
        lazy='dynamic'
    )

    user_recipes = database.relationship(
        'RecipeBox',
        backref='user',
        lazy='dynamic'
    )

    followed = database.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=database.backref('followers', lazy='dynamic'), lazy='dynamic')

    user_meals = database.relationship(
        "Meal",
        backref='user',
        lazy='dynamic'
    )        

    def is_password_correct(self, password_plaintext: str):
        return bcrypt.check_password_hash(self.password_hashed, password_plaintext)


    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return bcrypt.generate_password_hash(
            password_plaintext,
            current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
    
    def __repr__(self):
        return f'<User: {self.email} {self.password_hashed}>'

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

    id = database.Column(
        database.Integer,
        primary_key=True
    )

    username = database.Column(
        database.String,
        nullable=False
    )
    
    first_name = database.Column(
        database.String, 
        nullable=True
    )

    last_name = database.Column(
        database.String, 
        nullable=True
    )

    user_id = database.Column(
        database.Integer, 
        database.ForeignKey('users.id')
    ) 

    def __init__(self, username: str, first_name: str, last_name: str, user_id: int):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        
    def __repr__(self):
        """ Show info about user_profile. """

        u = self
        return f"<UserProfile {u.username} {u.first_name} {u.last_name}"

class RecipeBox(database.Model):
    """
    Class that represents a user's recipe box (liked recipes, stored in the database).

    The following attributes of a user are stored in this table:
        is_liked (type: boolean) 
        user_id (type: int)
        recipe_id (type: int)

    All three values are required.
    """

    __tablename__ = 'recipe_boxes'

    id = database.Column(
        database.Integer,
        primary_key=True
    )

    is_liked = database.Column(
        database.Boolean,
        nullable=False,
        default=True
    )

    recipe_url = database.Column(
        database.String,
        nullable=False
    ) 

    user_id = database.Column(
        database.Integer, 
        database.ForeignKey('users.id', ondelete='cascade')
    )

    __table_args__ = (
        database.UniqueConstraint('user_id', 'recipe_url'),
    )

    def __init__(self, is_liked: bool, recipe_url: str, user_id: int):
        self.is_liked = is_liked
        self.recipe_url = recipe_url
        self.user_id = user_id



    
## Meal Planner
class Meal(database.Model):
    """
    Class that handles a user's meal planning.

    Users can add items from their saved recipe box to create meals.

    The following attributes of a meal are stored in this table:
        * meal_date: The date a user plans to have a meal (required)
        * meal_title: The (optional) title of the meal, assigned by the user (not required).
        * meal_notes: The (optional) notes about the meal, provided by the user (not required).
        * recipe_id: The Spoonacular recipe_id (Required).
        * recipe_title: The Spoonacular recipe_title (Required).
        * recipe_url: The source URL of the recipe (Required).
        * user_id: The user_id (Foreign key from User table; required).
    """
    
    __tablename__ = 'meals'

    id = database.Column(
        database.Integer,
        primary_key=True
    )
    
    meal_date = database.Column(
        database.DateTime,
        nullable = False,
        default = datetime.now()
    )
  
    meal_title = database.Column(
        database.String(100), 
        nullable = True
    )

    meal_notes = database.Column(
        database.String(1000), 
        nullable = True
    )

    recipe_id = database.Column(
        database.Integer, 
        nullable = False
    )

    recipe_title = database.Column(
        database.String, 
        nullable = False
    )

    recipe_url = database.Column(
        database.String, 
        nullable = False
    )

    user_id = database.Column(
        database.Integer, 
        database.ForeignKey('users.id')
    ) 


    def __init__(self, meal_date: datetime, meal_title: str, meal_notes: str, recipe_id: int, recipe_title: str, recipe_url: str, user_id: int):
        self.meal_date = meal_date
        self.meal_title = meal_title
        self.meal_notes = meal_notes
        
        self.recipe_id = recipe_id
        self.recipe_title = recipe_title
        self.recipe_url = recipe_url
        self.user_id = user_id
        
