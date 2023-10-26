# Local library imports
from gameping.database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(255), unique=True)
    carrier = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.name!r}>'
