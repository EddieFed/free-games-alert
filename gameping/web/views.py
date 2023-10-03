from flask import render_template, Blueprint, redirect, url_for, request
from gameping import db
from gameping.models import ContactsModel, LatestModel
from jobs.mailer import send_confirmation

web_blueprint = Blueprint('web', __name__)


# localhost:5000 will access this entrypoint & render template from login.html
@web_blueprint.route('/')
def index():
    return redirect(url_for('web.signmeup'))


@web_blueprint.route('/signmeup', methods=['POST', 'GET'])
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
                send_confirmation(phone, carrier)

                data = ContactsModel(name, phone, carrier, email)
                db.session.add(data)
                db.session.commit()
                return render_template('signmeup.html', response="success")
            else:
                return render_template('signmeup.html', response="inSystem")
    else:
        return render_template('signmeup.html')


@web_blueprint.route('/takemeoff', methods=['POST', 'GET'])
def takemeoff():
    if request.method == 'POST':
        phone = request.form['phone'].replace('-', '')
        remove = db.session.query(ContactsModel).filter(ContactsModel.phone == phone).first()
        db.session.delete(remove)
        db.session.commit()
        return render_template('takemeoff.html', response="goodbye")

    else:
        return render_template('takemeoff.html')


@web_blueprint.route('/faq')
def faq():
    return render_template('faq.html')


@web_blueprint.route('/debug')
def debug():
    contacts = db.session.query(ContactsModel).all()
    for person in contacts:
        print(person.name, person.phone, person.carrier, person.email)
    return 'Nothing to see here!'
