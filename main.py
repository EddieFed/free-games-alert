"""
This is a simple project made to alert me any time a new game is available for free

Data is sourced by indiegamebundles.com
"""
import smtplib
import requests
from bs4 import BeautifulSoup

import random

from_addr = 'alert.free.games@gmail.com'
# recipients = ['6309408929@mms.att.net', '6309408226@mms.att.net', '6307474342@mms.att.net', '6307474323@mms.att.net']
recipients = ['6309408929@mms.att.net', '8478487510@tmomail.net']

# Options to create custom message
phrases = ['Free Game!!!', 'Guess what? Free Game!', 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces = ['ᕕ(⌐■_■)ᕗ ♪♬', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '_|___|_  ╰(º o º╰)', 'ᕕ( ・‿・)つ-●-●']


def send_mail(name: str, link: str):
    """
    :param name The name of the game
    :param link The link to the article
    Builds an email that will be sent to an mms gateway
    """
    body = '%s\n.\n%s\n.\n%s\n%s' % (random.choice(phrases), random.choice(faces), name, link)
    body = body.encode('utf-8')

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(from_addr, 'jjlol123')
    server.sendmail(from_addr, recipients, body)


# Sends a request for the entire page on IndieGameBundles
r = requests.get('https://www.indiegamebundles.com/category/free/')
r = r.text
soup = BeautifulSoup(r, 'html.parser')

# Grabs the specific container that contains the latest post on the site
game = soup.find(class_='td-pb-span8 td-main-content').find(class_='entry-title td-module-title')

# We will use a text file to store the most recent article title on the website
latest = open('latest.txt', 'r')

# If the latest title received from the site doesn't match the title stored, that means there is a new game available!
if latest.read() != game.get_text():
    print('New game!')
    send_mail(name=game.get_text(), link=game.a.get('href'))
    latest = open('latest.txt', 'w')
    latest.write(game.get_text())
    latest.close()
else:
    print('No new game at this time!')


