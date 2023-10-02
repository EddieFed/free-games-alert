from app.app import db


class LatestModel(db.Model):
    __tablename__ = 'games'
    i = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    game = db.Column(db.VARCHAR(200))

    def __init__(self, game):
        self.game = game
