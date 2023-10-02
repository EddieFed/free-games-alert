from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

# Local references
from scraper import scrape
from confirm import confirm_number
from mailer import send_confirmation
from config.settings import settings

app = Flask(__name__)

# Init SQLAlchemy
app.debug = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if settings is None:
    print('Running with hardcoded login below...\n')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://username:password@localhost/gameping'

else:
    # Since settings file exists, we can use the login stored in there
    print('Running with config/settings.json')
    db_login = settings["db"]
    app.config['SQLALCHEMY_DATABASE_URI'] = (f"{db_login['database']}{db_login['engine']}://"
                                             f"{db_login['username']}:{db_login['password']}@{db_login['address']}")

db = SQLAlchemy(app)
app.app_context().push()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_job("scrape-job", scrape, trigger="cron", minute="0,30", jitter=(2 * 60))
scheduler.add_job("confirm-job", confirm_number, trigger="cron", minute="*", jitter=(2 * 60))
scheduler.start()


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
                send_confirmation(phone, carrier)

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
