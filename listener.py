# coding=utf-8
"""
    This is a simple project made to alert me any time a new game is available for free
    Data is sourced by www.indiegamebundles.com

    Copyright 2019 Eddie Federmeyer
"""
import json
import random
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Local references
from app import db, ContactsModel, LatestModel
from config.vars import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER

# Message Decor
phrases = ['Guess what? Free Game!', 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces = ['ᕕ(⌐■_■)ᕗ ♪♬', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '_|___|_  ╰(º o º╰)', 'ᕕ( ・‿・)つ-●-●']


def send_mail(game: str, link: str, recipient: str, image_link: str) -> None:
    message = MIMEMultipart()
    message['FROM'] = EMAIL_ADDRESS
    message['TO'] = recipient
    message['SUBJECT'] = random.choice(phrases)
    message.attach(MIMEText(random.choice(faces) + '\n.\n' + game + '\n' + link, 'plain'))

    # Open image in binary mode
    with requests.get(image_link) as attachment:
        part = MIMEImage(attachment.content)
        message.attach(part)

    server = smtplib.SMTP(host=SMTP_SERVER, port=587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, recipient, message.as_string())

    print('Mail sent to "', recipient, '"!')
    return None


def __main__():
    # Sends a request for the entire page on IndieGameBundles
    res = requests.get('https://www.indiegamebundles.com/category/free/')
    res = res.text
    soup = BeautifulSoup(res, 'html.parser')

    # Grabs the specific container that contains the latest post on the site
    game_data = soup.find(class_='td-module-thumb')
    game = game_data.a['title']
    link = game_data.a['href']
    image_link = game_data.a.span['data-bg']

    # Double checks that the game is different then the latest free game
    if db.session.query(LatestModel).filter(LatestModel.game == game).count() == 0:
        # Write the new game to the db so I don't forget...
        db_latest_data = LatestModel(game)
        db.session.add(db_latest_data)
        db.session.commit()

        # We will get gateway data from carriers.json
        # And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
        carriers = json.load(open('carriers.json', 'r'))

        # Double checks if any contacts exist
        if db.session.query(ContactsModel).filter(ContactsModel.send == True).count() == 0:
            print('Please confirm a contact before running')
            return

        # For every contact, format sms gateway
        for contact in db.session.query(ContactsModel).filter(ContactsModel.send == True).all():
            # Formats recipient address
            recipient = contact.phone + '@' + carriers[contact.carrier]
            send_mail(game=game, link=link, recipient=recipient, image_link=image_link)

        print('Mailing list finished!')

    else:
        print('No new game!')


if __name__ == '__main__':
    __main__()
