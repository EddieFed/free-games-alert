"""
Usage:
    python build.py py2app

    TODO:
    - Make cross platform build script
"""

from setuptools import setup

APP_NAME = "free-games-alert"
APP = ["main.py"]
DATA_FILES = ["phone.json, latest.txt"]
OPTIONS = {
    "argv_emulation": True,
    "packages": ["json", "requests", "bs4", "random", "smtplib", "email"]
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    py_modules=["new_contact.py"]
)
