# coding=utf-8
"""
This is a super generic command line tool to add a person to the list of recipients

Copyright 2020 Eddie Federmeyer
"""
import json

try:
    with open("phone.json", "r+") as file:
        tmp_json: dict = json.load(file)

        name: str = input("Name: ")
        number: str = input("Number (Format - xxxyyyzzz): ")
        carrier: str = input("carrier (Options - att, tmobile, boost, metro, sprint, verizon, cricket): ")

        tmp_json["contacts"][name] = {"phone": number, "carrier": carrier}

        file.write(json.loads(tmp_json), file)

except IOError:
    print("File does not exist")
