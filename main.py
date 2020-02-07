"""
    TODO:
    - Make universal entry point
"""

import new_contact
import listener
import os
import sys

import tkinter

root = tkinter.Tk()
label = tkinter.Label(master=root, text="Name:")
label.pack(side=tkinter.LEFT)
textbox = tkinter.Entry(master=root)
# textbox.insert(0, "What is your name?")
textbox.pack()
button = tkinter.Button(master=root, text="Hello!")
button.pack()
tkinter.mainloop()

sys.exit(0)

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


