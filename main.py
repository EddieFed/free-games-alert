"""
    TODO:
    - Make universal entry point
"""

import new_contact
import listener
import os
import pathlib
import sys

app_path = ""
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
elif __file__:
    app_path = os.path.dirname(__file__)

print(app_path)

while True:
    cmd = input("Please type\n"
                " - 'phone' to add a new contact\n"
                " - 'start' to start the listener\n"
                " - 'exit' to quit\n"
                "--> ")

    if cmd.lower() == "phone":
        new_contact.__main__(app_path)
    elif cmd.lower() == "start":
        listener.__main__(app_path)
    elif cmd.lower() == "exit":
        sys.exit(0)
    else:
        print("That's not a valid command, please run again")


