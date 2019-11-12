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
recipients = ['6309408929@mms.att.net']

phrases = ['Free Game!!!', 'Guess what? Free Game!', 'Here\'s a free game for you!', 'Enjoy a free game!', 'Surprise!']
faces = ['ᕕ(⌐■_■)ᕗ ♪♬']


def send_mail(name, link):
    body = '%s\n%s\n%s\n%s' % (random.choice(phrases), random.choice(faces), name, link)
    body = body.encode('utf-8')

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(from_addr, 'jjlol123')
    server.sendmail(from_addr, recipients, body)


r = requests.get('https://www.indiegamebundles.com/category/free/')
r = r.text
soup = BeautifulSoup(r, 'html.parser')

game = soup.find(class_='td-pb-span8 td-main-content').find(class_='entry-title td-module-title')

latest = open('latest.txt', 'r')
if latest.read() != game.get_text():
    send_mail(name=game.get_text(), link=game.a.get('href'))
    latest = open('latest.txt', 'w')
    latest.write(game.get_text())
    latest.close()
else:
    print('No new game at this time!')


