# coding=utf-8
"""
This is a simple project made to alert me any time a new game is available for free

Data is sourced by indiegamebundles.com

Copyright 2019 Eddie Federmeyer
"""
import smtplib
import requests
from bs4 import BeautifulSoup
import random
import json


smtp_server: str = 'smtp.gmail.com'

from_addr: str = 'alert.free.games@gmail.com'
recipients: list = ['eddie']

# Options to create custom message
phrases: list = ['Free Game!!!', 'Guess what? Free Game!',
                 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces: list = ['ᕕ(⌐■_■)ᕗ ♪♬', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '_|___|_  ╰(º o º╰)', 'ᕕ( ・‿・)つ-●-●']


def send_mail(g: str, link: str, addr: str) -> None:
    """
    :param addr: Email of the recipient
    :param g: The name of the game
    :param link: The link to the article
    Builds an email that will be sent to an mms gateway
    """
    subj = random.choice(phrases)

    message = '%s\n.\n%s\n.\n%s\n%s' % (random.choice(phrases), random.choice(faces), g, link)

    body = """From: Free Games! <Alert.Free.Games@gmail.com>
To: Person! <%s>
Subject: 
%s""" % (addr, message)

    body = body.encode('utf-8')

    print(body)

    server = smtplib.SMTP(host=smtp_server, port=587)
    server.starttls()
    server.login(from_addr, 'jjlol123')
    server.sendmail(from_addr, addr, body)


# Sends a request for the entire page on IndieGameBundles
r = requests.get('https://www.indiegamebundles.com/category/free/')
r = r.text
soup = BeautifulSoup(r, 'html.parser')

# Grabs the specific container that contains the latest post on the site
game = soup.find(class_='td-pb-span8 td-main-content').find(class_='entry-title td-module-title')

# We will use a text file to store the most recent article title on the website
latest = open('latest.txt', 'w')


# If the latest title received from the site doesn't match the title stored, that means there is a new game available!
#
# TODO
# for production -> if latest.read() != game.get_text():

# We will get phone data from phone.json
# And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
phone_json: dict = json.load(open('phone.json', 'r'))
for name in recipients:

    # Formats recipient address
    recipient: str = phone_json['contacts'][name]['phone'] + '@' + \
                phone_json['carriers'][phone_json['contacts'][name]['carrier']]
    # send_mail(g=game.get_text(), link=game.a.get('href'), addr=recipient)
    send_mail("game", "https://www.example.com", recipient)
# latest.write(game.get_text())
# latest.close()
