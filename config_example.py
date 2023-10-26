# System library imports
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or 'this is my secret key!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'mysql+mysqlconnector://username:pasword@localhost/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
