"""
This is a simple project made to alert me any time a new game is available for free

Data is sourced by indiegamebundles.com

Copyright 2019 Eddie Federmeyer
"""
import smtplib
import requests
from bs4 import BeautifulSoup
import random


from_addr = 'alert.free.games@gmail.com'
# recipients = ['6309408929@mms.att.net', '6309408226@mms.att.net', '6307474342@mms.att.net', '6307474323@mms.att.net'] # Eddie, Tommy, Mom, Dad
# recipients = ['6309408929@mms.att.net', '8478487510@tmomail.net', '8478109442@tmomail.net', '8477497533@tmomail.net'] # Eddie, Johnny, Kevin, Sule
# recipients = ['8478487510@tmomail.net'] # Kevin
# recipients = ['6309408929@mms.att.net', '6304562592@tmomail.net'] # Eddie, Murat
# recipients = ['6309408929@mms.att.net'] # Eddie
recipients = ['6304562592@tmomail.net']

# Options to create custom message
phrases = ['Free Game!!!', 'Guess what? Free Game!', 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces = ['ᕕ(⌐■_■)ᕗ ♪♬', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '_|___|_  ╰(º o º╰)', 'ᕕ( ・‿・)つ-●-●']


def send_mail(name: str, link: str, addr: str):
    """
    :param name The name of the game
    :param link The link to the article
    Builds an email that will be sent to an mms gateway
    """
    subj = random.choice(phrases)
    # body = 'From%s\n.\n%s\n.\n%s\n%s' % (random.choice(phrases), random.choice(faces), name, link)

    # From: alert.free.games@gmail.com
    # To: xxxxxxxxxx@something.net
    # Subject: ''

    message = '%s\n.\n%s\n.\n%s\n%s' % (random.choice(phrases), random.choice(faces), name, link)

    body = """From: Free Games! <Alert.Free.Games@gmail.com>
To: Person! <%s>
Subject: 
%s""" % (addr, message)
    body = body.encode('utf-8')

    print(body)

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
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
latest = open('latest.txt', 'r')

# If the latest title received from the site doesn't match the title stored, that means there is a new game available!
#if latest.read() != game.get_text():
if True == True:
    print('New game!')

    # Since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
    for number in recipients:
        send_mail(name=game.get_text(), link=game.a.get('href'), addr=number)
    latest = open('latest.txt', 'w')
    latest.write(game.get_text())
    latest.close()
else:
    print('No new game at this time!')


