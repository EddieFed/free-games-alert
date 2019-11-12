"""
This is a simple project made to alert me any time a new game is available for free

Data is sourced by indiegamebundles.com
"""
import smtplib
import requests
from bs4 import BeautifulSoup

from_addr = 'alert.free.games@gmail.com'
# recipients = ['6309408929@mms.att.net', '6309408226@mms.att.net', '6307474342@mms.att.net', '6307474323@mms.att.net']
recipients = ['6309408929@mms.att.net']

#body = """Guess What %s
#There's a new free game at
#%s!""" % ('Eddie', 'http://localhost/')

r = requests.get('https://www.indiegamebundles.com/category/free/')
r = r.text

soup = BeautifulSoup(r, 'html.parser')

# games = []
# for h3 in soup.find(class_='td-pb-span8 td-main-content').find_all(class_='entry-title td-module-title'):
#    game = h3.a.get_text()
#    games.append(game)
#    print(game)

game = soup.find(class_='td-pb-span8 td-main-content').find(class_='entry-title td-module-title')

body = """New game for free!
%s

%s""" % (game.get_text(), game.a.get('href')) 

# body = ('\n'.join(map(str, games))).encode(encoding='utf-8')


server = smtplib.SMTP(host='smtp.gmail.com', port=587)
server.starttls()
server.login(from_addr, 'jjlol123')
server.sendmail(from_addr, recipients, body)

