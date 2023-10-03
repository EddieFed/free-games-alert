# coding=utf-8
"""
    This is a simple project made to alert me any time a new game is available for free
    Data is sourced by www.indiegamebundles.com

    Copyright 2019 Eddie Federmeyer
"""
import json
import re
import random
from io import BytesIO
from PIL import Image
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup

# Local references
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))
# We need to add the child paths to the project! This is so BS...

from gameping import db
from gameping.models import ContactsModel, LatestModel
from gameping.jobs.mailer import send_gameping, send_message
from gameping.config.settings import settings


def scrape():
    print("Running web scraper!")
    # Sends a request for the entire page on IndieGameBundles
    display = Display(size=(600, 900), backend='xvfb')
    display.start()

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.indiegamebundles.com/category/free/')
    res = driver.page_source

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

    im = im.crop((width - 696, 0, width, height))
    im.save(img, "PNG")

    driver.quit()
    display.stop()

    # Double checks that the game is different from the latest free game
    if db.session.query(LatestModel).filter(LatestModel.game == game).count() == 0:
        # Write the new game to the db, so I don't forget...
        db_latest_data = LatestModel(game)
        db.session.add(db_latest_data)
        db.session.commit()

        # We will get gateway data from carriers.json
        # And since Emails must be sent one at a time because T-Mobile is a bitch I gotta use a loop
        carriers = settings["carriers"]

        # Double checks if any contacts exist
        if db.session.query(ContactsModel).filter(ContactsModel.send is True).count() == 0:
            print('Please confirm a contact before running')
            return

        # For every contact, format sms gateway
        for contact in db.session.query(ContactsModel).filter(ContactsModel.send is True).all():
            # Formats recipient address
            recipient = f"{contact.phone}@{carriers[contact.carrier]}"
            subject = random.choice(settings["messages"])
            msg = random.choice(settings["flair"])

            send_gameping(game=game, link=link, recipient=recipient, img=img, subject=subject, msg=msg)

        print('Mailing list finished!')

    else:
        send_message(recipient="6309408929@mms.att.net", subject="Debug", msg="No new game!")
        print('No new game!')


if __name__ == '__main__':
    scrape()
