# External library imports
from flask import render_template, redirect, url_for, request, Response

# Local library imports
from gameping.web import bp
from gameping.database import db
from gameping.models import User


@bp.route('/')
def index() -> Response:
    return redirect(url_for('web.signup'))


@bp.route('/signup', methods=['POST', 'GET'])
def signup() -> str:
    if request.method == 'POST':
        name: str       = request.form['name']
        phone: str      = request.form['phone'].replace('-', '')
        carrier: str    = request.form['carrier']
        email: str      = request.form['email'] or ''

        print(f'Received request with: {name}, {phone}, {carrier}, {email}')
        if name == '' or phone == '':
            return 'Please include all required info'
        else:
            if db.session.query(User).filter(User.phone == phone).count() == 0:
                # mailer.send_confirmation(phone, carrier)

                data = User()
                data.name = name
                data.phone = phone
                data.carrier = carrier
                data.email = email
                db.session.add(data)
                db.session.commit()
                return render_template('signup.html', response="success")
            else:
                return render_template('signup.html', response="inSystem")
    else:
        return render_template('signup.html')


@bp.route('/remove', methods=['POST', 'GET'])
def remove() -> str:
    if request.method == 'POST':
        phone = request.form['phone'].replace('-', '')
        user = db.session.query(User).filter(User.phone == phone).first()
        db.session.delete(user)
        db.session.commit()
        return render_template('remove.html', response="goodbye")

    else:
        return render_template('remove.html')


@bp.route('/faq')
def faq() -> str:
    return render_template('faq.html')


@bp.route('/debug')
def debug() -> str:
    users = db.session.query(User).all()
    for person in users:
        print(person.name, person.phone, person.carrier, person.email)
    return 'Nothing to see here!'
