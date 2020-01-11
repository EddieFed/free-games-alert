# coding=utf-8
"""
This is a simple project made to alert me any time a new game is available for free

Data is sourced by indiegamebundles.com

Copyright 2019 Eddie Federmeyer
"""
import json
import random
import requests
import smtplib

from bs4 import BeautifulSoup
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server: str = 'smtp.gmail.com'
phrases: list = ['Guess what? Free Game!', 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces: list = ['ᕕ(⌐■_■)ᕗ ♪♬', '╰(✿˙ᗜ˙)੭━☆ﾟ.*･｡ﾟ', '_|___|_  ╰(º o º╰)', 'ᕕ( ・‿・)つ-●-●']

from_addr: str = 'alert.free.games@gmail.com'
recipients: list = ['eddie', 'murat']


def send_mail(rec: str, t: str) -> None:
    """
    :param rec: Email of the recipient
    :param t: The name of the game
    Sends email through mms gateway
    """

    server = smtplib.SMTP(host=smtp_server, port=587)
    server.starttls()
    server.login(from_addr, 'jjlol123')
    server.sendmail(from_addr, rec, t)


def formulate_mail(g: str, li: str, rec: str, i: str) -> str:
    """
        :param g: Game
        :param li: Link
        :param rec: Recipient
        :param i: Image
        Builds an MIME email
    """

    message = MIMEMultipart()
    message['FROM'] = from_addr
    message['TO'] = rec
    message['SUBJECT'] = random.choice(phrases)
    message.attach(MIMEText(random.choice(faces) + '\n.\n' + g + '\n' + li, 'plain'))

    # Open image in binary mode
    with requests.get(i) as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.content)

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment; filename=image.jpg",
    )
    message.attach(part)
    return message.as_string()


# Sends a request for the entire page on IndieGameBundles
r = requests.get('https://www.indiegamebundles.com/category/free/')
r = r.text
soup = BeautifulSoup(r, 'html.parser')

# Grabs the specific container that contains the latest post on the site
game_data = soup.find(class_='entry-title td-module-title')
game = game_data.get_text()
link = game_data.a['href']
image_link = soup.find(class_='td-image-wrap').img['data-img-url']

# We will use a text file to store the most recent article title on the website
latest = open('latest.txt', 'r+')

# We will get phone data from phone.json
# And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
# If the latest title received from the site doesn't match the title stored, that means there is a new game available!
phone_json: dict = json.load(open('phone.json', 'r'))
if latest.read() != game:
    for name in recipients:

        # Formats recipient address
        recipient: str = phone_json['contacts'][name]['phone'] + '@' + \
                    phone_json['carriers'][phone_json['contacts'][name]['carrier']]
        body_text = formulate_mail(g=game, li=link, rec=recipient, i=image_link)
        send_mail(rec=recipient, t=body_text)

    print('Mail sent!')
    latest.write(game)
    latest.close()
else:
    print('No new game!')
