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

# Load settings // Replace with enviroment var refs
#
# If getting errors with authentication and using gmail.
# visit https://myaccount.google.com/lesssecureapps to unlock email
settings = json.load(open('./settings.json', 'r+'))
smtp_server = settings['smtp server'] or None
from_addr = settings['email'] or None
password = settings['password'] or None

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

    # We will use a text file to store the most recent article title on the website
    latest = open('./latest.txt', 'r+')
    # Double checks that the game is different then the previous free game
    if latest.read() != game:
        # Write the new game to the file so I don't forget...
        latest.write(game)
        latest.close()

        # We will get phone data from phone.json
        # And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
        # If the latest title received from the site doesn't match the title stored,
        # That means there is a new game available!
        phone_json = json.load(open('./phone.json', 'r'))

        # Double checks if any contacts exist
        if len(phone_json['contacts']) == 0:
            print('Please add a contact before running')
            return

        # For every contact, format sms gateway
        for contact in phone_json['contacts']:
            # Formats recipient address
            recipient = contact['phone'] + '@' + phone_json['carriers'][contact['carrier']]
            # body_text = formulate_mail(g=game, li=link, rec=recipient, i=image_link)
            # send_mail(rec=recipient, t=body_text)
            send_mail(game=game, link=link, recipient=recipient, image_link=image_link)

        print('Mailing list finished!')

    else:
        print('No new game!')


__main__()
