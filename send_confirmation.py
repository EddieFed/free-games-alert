import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Local references
from config.vars import SMTP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD


def confirm(recipient: str, msg=''):
    message = MIMEMultipart()
    message['FROM'] = EMAIL_ADDRESS
    message['TO'] = recipient
    message['SUBJECT'] = ''
    message.attach(MIMEText(msg, 'plain'))

    server = smtplib.SMTP(host=SMTP_SERVER, port=587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, recipient, message.as_string())

    print('Confirmation sent to "', recipient, '"!')
    return None
