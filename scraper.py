# coding=utf-8
"""
    This is a simple project made to alert me any time a new game is available for free
    Data is sourced by www.indiegamebundles.com

    Copyright 2019 Eddie Federmeyer
"""
import json
import re
import random
import requests
from io import BytesIO
from PIL import Image
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup

# Local references
from app import db, ContactsModel, LatestModel
from mailer import send_gameping
from config.settings import settings


def __main__():
    # Sends a request for the entire page on IndieGameBundles
    with Display(visible=0, size=(696, 392)) as display:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.indiegamebundles.com/category/free/')
        res = driver.page_source

        # driver.quit()

        soup = BeautifulSoup(res, 'html.parser')

        # Grabs the specific container that contains the latest post on the site
        game_data = soup.find(class_='td-image-wrap')
        print(game_data)
        game = game_data['title']
        link = game_data['href']
        image_link = game_data.span['style']
        image_link = re.search(r"url\((.*)\)", image_link).group(1)
    
        # Get actual image
        driver.get(image_link)
        img = BytesIO(driver.get_screenshot_as_png())
        
        im = Image.open(img)
        width, height = im.size

        im = im.crop((width-696, 0, width, height))
        im.save(img, "PNG")

        # res2 = requests.get(image_link)
        # print(res2.content)
        # img = BytesIO(res2.content)

        driver.quit()

    # Double checks that the game is different from the latest free game
    if db.session.query(LatestModel).filter(LatestModel.game == game).count() == 0:
        # Write the new game to the db, so I don't forget...
        db_latest_data = LatestModel(game)
        db.session.add(db_latest_data)
        db.session.commit()

        # We will get gateway data from carriers.json
        # And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
        carriers = json.load(open('config/carriers.json', 'r'))

        # Double checks if any contacts exist
        if db.session.query(ContactsModel).filter(ContactsModel.send == True).count() == 0:
            print('Please confirm a contact before running')
            return

        # For every contact, format sms gateway
        for contact in db.session.query(ContactsModel).filter(ContactsModel.send == True).all():
        # for name in ["eddie"]:
            # recipient = "6309408929@mms.att.net"
            # Formats recipient address
            recipient = contact.phone + '@' + carriers[contact.carrier]
            send_gameping(game=game, link=link, recipient=recipient, img=img,
                          subject=random.choice(settings["messages"]), msg=random.choice(settings["flair"]))

        print('Mailing list finished!')

    else:
        print('No new game!')


if __name__ == '__main__':
    __main__()
