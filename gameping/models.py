import sqlalchemy as sa
from gameping import db  # import db instance from __init__.py in gaming directory


class ContactsModel(db.Model):
    __tablename__ = 'contacts'
    name = sa.Column(sa.String(50), primary_key=True)
    phone = sa.Column(sa.String(10), unique=True)
    carrier = sa.Column(sa.String())
    email = sa.Column(sa.String())
    confirmed = sa.Column(sa.Boolean(), default=False)

    def __init__(self, name, phone, carrier, email):
        self.name = name
        self.phone = phone
        self.carrier = carrier
        self.email = email


class LatestModel(db.Model):
    __tablename__ = 'games'
    i = sa.Column(sa.Integer(), autoincrement=True, primary_key=True)
    time = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())
    game = sa.Column(sa.String(255))

    def __init__(self, game):
        self.game = game
