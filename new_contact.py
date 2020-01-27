# coding=utf-8
"""
This is a super generic command line tool to add a person to the list of recipients

Copyright 2020 Eddie Federmeyer
"""
import json


def __main__():
    try:

        with open("phone.json", "r+") as file:
            tmp_json: dict = json.load(file)

            name: str = input("Name: ")
            while True:
                number: str = input("Number (Format - xxxyyyzzzz): ")
                if number.isnumeric() and len(number) == 10:
                    break
                else:
                    print("Either too long or not a number! Try again!")
                    pass

            while True:
                carrier: str = input("carrier (Options - att, tmobile, boost, metro, sprint, verizon, cricket): ")
                if tmp_json["carriers"].keys().__contains__(carrier):
                    break
                else:
                    print("Not a valid carrier! Try again!")
                    pass

            tmp_json["contacts"][name] = {"phone": number, "carrier": carrier}

            file.seek(0)
            file.write(json.dumps(tmp_json, indent=4, sort_keys=True))
            file.close()

    except IOError:
        print("File does not exist, did you delete it?")


__main__()
