# Eddie's Free Games Alert!
#### A simple mms messenger that will let you know what's free!

# ** new_contact.py and main.py are useless for now, simply run listener.py if you'd like to try this... **

One day I realized how many free games I was missing from humble bundle, steam, epic games, etc.
So I thought I'd whip this up real quick.

It just uses [IndieGameBundles](https://www.indiegamebundles.com/category/free/ "IndieGameBundles") as it's source for information (will probably be expanded soon)

Currently, this just will let you know when _anything_ new is listed on the site. Hopefully I can update this to include a way to send alerts according to preferences

# Setup
To set this up you'll need Python 3.7+

Then you will want to install the following with pip.
* requests
* bs4

After those are added to the python enviroment, rename `settings_example.json` to `settings.json`.

# Some notes and ToDo's
* For now, you'll need to manually add a contact to the list in `settings.json` but soon I'll fix the other script that deals with that...
* There is no automation implemented yet. I'd say for now it's best to schedule running this as a task every hour or so. Ideally ill fix this too soon
* Eventually I'll be deploying this to (gameping.eddiefed.com)[https://gameping.eddiefed.com] so anyone can sign up to be added (and removed) to the list but that's for later...
