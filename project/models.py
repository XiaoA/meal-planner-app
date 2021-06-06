from project import database


class User(database.Model):
    """
    Class that represents a user of the site.

    The following attributes of a stock are stored in this table:
        stock symbol (type: string)
        number of shares (type: integer)
        purchase price (type: integer)

    Note: Due to a limitation in the data types supported by SQLite, the
          purchase price is stored as an integer:
              $24.10 -> 2410
              $100.00 -> 10000
              $87.65 -> 8765
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
