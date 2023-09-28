# coding=utf-8
import os
import json

# Load settings file
#
# If getting errors with authentication and using gmail.
# visit https://myaccount.google.com/lesssecureapps to unlock email
# Get reference to settings file
settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "settings.json")
settings = json.load(open(settings_path, 'rb+'))
