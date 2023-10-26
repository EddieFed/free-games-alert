# Local library imports
from gameping.database import db


class Game(db.Model):
    __tablename__ = 'games'
    i = db.Column(db.Integer(), autoincrement=True, primary_key=True, unique=True)
    game = db.Column(db.String(255), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def __repr__(self):
        return f'<Game {self.game!r}>'
