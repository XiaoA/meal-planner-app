from project import database


class User(database.Model):
    """
    Class that represents a user of the site. (Note: authentication is handled outside of the User model.)

    The following attributes of a stock are stored in this table:
        username (type: string) 
        first_name (type: string) 
        last_name (type: string)

    The username and first_name attributes are required; last_name is optional.
    """

    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    first_name = database.Column(database.String, nullable=False)
    first_name = database.Column(database.String, nullable=True)

    def __init__(self, username: str, first_name: str, last_name: str):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        """ Show info about user. """

        u = self
        return f"<User {u.id} {u.username} {u.first_name} {u.last_name}"
