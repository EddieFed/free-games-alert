# coding=utf-8
"""
    This is a simple project made to alert me any time a new game is available for free
    Data is sourced by www.indiegamebundles.com

    Copyright 2019 Eddie Federmeyer
"""
import json
from random import Random
import requests
from bs4 import BeautifulSoup

# Local references
from app import db, ContactsModel, LatestModel
from mailer import send_gameping
from config.settings import settings


def __main__():
    # Sends a request for the entire page on IndieGameBundles
    res     = requests.get('https://www.indiegamebundles.com/category/free/')
    res     = res.text
    soup    = BeautifulSoup(res, 'html.parser')

    # Grabs the specific container that contains the latest post on the site
    game_data   = soup.find(class_='td-module-thumb')
    game        = game_data.a['title']
    link        = game_data.a['href']
    image_link  = game_data.a.span['data-bg']

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
            send_gameping(game=game, link=link, recipient=recipient, image_link=image_link, subject=Random.choice(settings["messages"]), message=Random.choice(settings["flair"]))

        print('Mailing list finished!')

    else:
        print('No new game!')


if __name__ == '__main__':
    __main__()
