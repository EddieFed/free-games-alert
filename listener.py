# coding=utf-8
"""
    This is a simple project made to alert me any time a new game is available for free
    Data is sourced by www.indiegamebundles.com

    Copyright 2019 Eddie Federmeyer
"""
import os
import json
import random
import requests
import smtplib

from bs4 import BeautifulSoup
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import db, ContactsModel, LatestModel


# Load settings
#
# If getting errors with authentication and using gmail.
# visit https://myaccount.google.com/lesssecureapps to unlock email
try:
    smtp_server = os.environ['smtp']
    from_addr = os.environ['email']
    password = os.environ['password']
except KeyError:
    print('Using local temp.json for settings...')
    temp = json.load(open('temp.json', 'r'))
    smtp_server = temp['smtp']
    from_addr = temp['email']
    password = temp['password']

# Message Decor
phrases = ['Guess what? Free Game!', 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces = ['ᕕ(⌐■_■)ᕗ ♪♬', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '_|___|_  ╰(º o º╰)', 'ᕕ( ・‿・)つ-●-●']


def send_mail(game: str, link: str, recipient: str, image_link: str) -> None:
    message = MIMEMultipart()
    message['FROM'] = from_addr
    message['TO'] = recipient
    message['SUBJECT'] = random.choice(phrases)
    message.attach(MIMEText(random.choice(faces) + '\n.\n' + game + '\n' + link, 'plain'))

    # Open image in binary mode
    with requests.get(image_link) as attachment:
        part = MIMEImage(attachment.content)
        message.attach(part)

    server = smtplib.SMTP(host=smtp_server, port=587)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, recipient, message.as_string())

    print('Mail sent to "', recipient, '"!')
    return None


def __main__():
    # Sends a request for the entire page on IndieGameBundles
    res = requests.get('https://www.indiegamebundles.com/category/free/')
    res = res.text
    soup = BeautifulSoup(res, 'html.parser')

    # Grabs the specific container that contains the latest post on the site
    game_data = soup.find(class_='entry-title td-module-title')
    game = game_data.get_text()
    link = game_data.a['href']
    image_link = soup.find(class_='td-image-wrap').img['data-img-url']

    # Double checks that the game is different then the latest free game
    if db.session.query(LatestModel).filter(LatestModel.game == game).count() == 0:
        # Write the new game to the db so I don't forget...
        db_latest_data = LatestModel(game)
        db.session.add(db_latest_data)
        db.session.commit()

        # We will get gateway data from carriers.json
        # And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
        carriers = json.load(open('./carriers.json', 'r'))

        # Double checks if any contacts exist
        if db.session.query(ContactsModel).count() == 0:
            print('Please add a contact before running')
            return

        # For every contact, format sms gateway
        for contact in db.session.query(ContactsModel).all():
            # Formats recipient address
            recipient = contact.phone + '@' + carriers[contact.carrier]
            send_mail(game=game, link=link, recipient=recipient, image_link=image_link)

        print('Mailing list finished!')

    else:
        print('No new game!')


if __name__ == '__main__':
    __main__()
