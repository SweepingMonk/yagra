"""
user module: contain User class and some functions
"""
from . import db


class User(object):
    """
    User class represents the normal user
    """

    def __init__(self):
        self.id_ = None
        self.email = None
        self.password = None
        self.default_image = None

    def auth(self):
        """
        authenticate current user, if correct return True,
        then load the other data into user object.
        if not correct, return False.
        """
        result = db.get_user_by_email(self.email)
        if result == None:
            return False
        elif result[2] != self.password:
            return False
        else:
            self.id_ = result[0]
            self.default_image = result[3]
            return True

    def exists(self):
        """
        testing the current user, if already exists return True,
        else return False
        """
        if db.get_user_by_email(self.email):
            return True
        else:
            return False

    def add_to_db(self):
        """
        add current user into database.
        """
        db.add_user(self.email, self.password)

    def save_default_image(self):
        """
        change user's default image.
        """
        db.change_default_image(self.id_, self.default_image)

    def save_password(self):
        """
        change user's password
        """
        db.change_password(self.id_, self.password)

