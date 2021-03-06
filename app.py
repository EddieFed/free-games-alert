from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import os

# Local references
from send_confirmation import confirm

app = Flask(__name__)

# Init SQLAlchemy
app.debug = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except KeyError:
    print('Running with test db...\n\n')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@192.168.1.140/test'


db = SQLAlchemy(app)


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


class LatestModel(db.Model):
    __tablename__ = 'latestgames'
    i = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    game = db.Column(db.VARCHAR(200))

    def __init__(self, game):
        self.game = game


@app.route('/')
def index():
    return redirect(url_for('signmeup'))


@app.route('/signmeup', methods=['POST', 'GET'])
def signmeup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone'].replace('-', '')
        carrier = request.form['carrier']
        email = request.form['email'] or ''
        print(name, phone, carrier, email)

        if name == '' or phone == '':
            return 'Please include all required info'
        else:
            if db.session.query(ContactsModel).filter(ContactsModel.phone == phone).count() == 0:
                message = 'Hello! thank you for adding your phone to gameping.eddiefed.com! Please respond with ' \
                          'YES if you want to opt in to receiving text messages! You can also respond with STOP at ' \
                          'any time to stop receiving messages or visit gameping.eddiefed.com/takemeoff'
                confirm(recipient=(phone + '@' + json.load(open('./carriers.json', 'r'))[carrier]), msg=message)
                data = ContactsModel(name, phone, carrier, email)
                db.session.add(data)
                db.session.commit()
                return render_template('signmeup.html', response="success")
            else:
                return render_template('signmeup.html', response="inSystem")
    else:
        return render_template('signmeup.html')


@app.route('/takemeoff', methods=['POST', 'GET'])
def takemeoff():
    if request.method == 'POST':
        phone = request.form['phone'].replace('-', '')
        remove = db.session.query(ContactsModel).filter(ContactsModel.phone == phone).first()
        db.session.delete(remove)
        db.session.commit()
        return render_template('takemeoff.html', response="goodbye")

    else:
        return render_template('takemeoff.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/debug')
def debug():
    contacts = db.session.query(ContactsModel).all()
    for person in contacts:
        print(person.name, person.phone, person.carrier, person.email)
    return 'Nothing to see here!'


if __name__ == '__main__':
    app.run()
