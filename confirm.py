# 
# This is a standalone script. Should be used by a cronjob or something similar
# to check mailboxes periodically
# 

import imaplib
import re

# Local references
from app import db, ContactsModel
from config.settings import settings

#
# Email init
email_address   = settings["email"]["address"]
email_password  = settings["email"]["password"]
email_imap      = settings["email"]["imap"]

# Connect to host
# Oh and by the way fuck IMAP, it's confusing...
imap = imaplib.IMAP4_SSL(email_imap)

# Login to server
imap.login(email_address, email_password)

# Select inbox
imap.select('INBOX')

# Search for all UNREAD messages. Message will be marked as read once this client receives it.
# Ignore rv, that's the response code. Not really important here.
# data however, IS important. The index data[0] is the sequence set used to fetch the corresponding message.
rv, data = imap.search(None, 'UNSEEN')
if len(data[0]) == 0:
    print('No new mail!')
    exit()

# We will use this to iterate through every sequence set that was send back from the search!
# Gotta split the byte tuple since it's, well raw bytes, not an array of the sequence sets.
for num in data[0].split(b' '):

    # raw_data here is complicated... At least to me...
    # Index raw_data[0] will be the FULL response for the first query (The body text)
    # Similarly raw_data[1] is the FULL response for the second query (The Headers)
    # To grab the actual data we need to use raw_data[i][1]
    rv, raw_data = imap.fetch(num, '(BODY[TEXT] BODY[HEADER.FIELDS (FROM)])')

    # The body text is the entire email body as a raw string... Yes I know, inefficient but whatever
    body_text = (raw_data[0][1]).decode().lower()

    # Since google periodically sends emails to this account, ignore all of them...
    if 'google' not in body_text:

        # Take out ONLY the numbers from the email, this will result in a pure phone number string.
        sender_text = re.sub("\\D", '', raw_data[1][1].decode())

        # This is to grab any sort of modification to the number (Like the 1 in the beginning)
        if len(sender_text) > 10:
            sender_text = sender_text[-10:]

        # I ned to grab the matching phone number from the database
        person = db.session.query(ContactsModel).filter(ContactsModel.phone == sender_text).first()

        # Here I do database stuffs!
        if 'yes' in body_text:
            print('Confirmed ' + sender_text)
            person.send = True

        elif 'stop' in body_text:
            print('Removed -> ' + sender_text)
            person.send = False

        db.session.commit()

