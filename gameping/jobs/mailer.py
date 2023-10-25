# 
# This is a generic script that is used to send emails
# can be imported and used by others
# 

import smtplib

from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Local references
from gameping.config.settings import settings

#
# Email init
email_address = settings["email"]["address"]
email_password = settings["email"]["password"]
email_smtp = settings["email"]["smtp"]


#
# 
def send_confirmation(phone: str, carrier: str) -> None:
    recipient = phone + '@' + settings["carriers"][carrier]

    message = MIMEMultipart()
    message['FROM'] = email_address
    message['TO'] = recipient
    message['SUBJECT'] = "Hello!"
    confirmation_msg = 'Thank you for adding your phone to gameping.eddiefed.com! Please respond with ' \
                       'YES if you want to opt in to receiving text messages! You can also respond with STOP at ' \
                       'any time to stop receiving messages or visit gameping.eddiefed.com/takemeoff'
    message.attach(MIMEText(confirmation_msg, 'plain'))

    send_mail(recipient, message)


#
# 
def send_gameping(game: str, link: str, recipient: str, msg: str, subject: str, img=None) -> None:
    message = MIMEMultipart()
    message['FROM'] = email_address
    message['TO'] = recipient
    message['SUBJECT'] = subject
    message.attach(MIMEText(msg + '\n.\n' + game + '\n' + link, 'plain'))

    if img is not None:
        part = MIMEImage(img.getvalue())
        message.attach(part)

    send_mail(recipient, message)


#
#
def send_message(recipient: str, subject: str = "", msg: str = "") -> None:
    message = MIMEMultipart()
    message['FROM'] = email_address
    message['TO'] = recipient
    message['SUBJECT'] = subject
    message.attach(MIMEText(f"{msg}"))

    send_mail(recipient, message)


#
# 
def send_mail(recipient: str, message: MIMEMultipart) -> None:
    server = smtplib.SMTP(host=email_smtp, port=587)
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, recipient, message.as_string())

    print(f'Mail sent to {recipient}!')
    return None
