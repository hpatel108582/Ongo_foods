"""
Instantiate and define database model definitions.
"""
# pylint: disable=no-member
# pylint: disable=redefined-builtin
# pylint: disable=too-few-public-methods
from app import db
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

class AuthUser(db.Model):
    """
    Defines AuthHistory table.
    """

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, userid, name, email):
        self.userid = userid
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.email)

