from app.app import db


class ContactsModel(db.Model):
    __tablename__ = 'contacts'
    name = db.Column(db.String(50), primary_key=True)
    phone = db.Column(db.String(10), unique=True)
    carrier = db.Column(db.String())
    email = db.Column(db.String())
    send = db.Column(db.Boolean(), default=False)

    def __init__(self, name, phone, carrier, email):
        self.name = name
        self.phone = phone
        self.carrier = carrier
        self.email = email
