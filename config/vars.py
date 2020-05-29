import os
import json


# Load settings
#
# If getting errors with authentication and using gmail.
# visit https://myaccount.google.com/lesssecureapps to unlock email
try:
    SMTP_SERVER = os.environ['smtp']
    IMAP_SERVER = os.environ['imap']
    EMAIL_ADDRESS = os.environ['email']
    EMAIL_PASSWORD = os.environ['password']
    print('Using production variables!')

except KeyError:
    temp = json.load(open('config/temp.json', 'r+'))

    SMTP_SERVER = temp['smtp']
    IMAP_SERVER = temp['imap']
    EMAIL_ADDRESS = temp['email']
    EMAIL_PASSWORD = temp['password']
    print('Using local temp.json for settings...')
