import os
from os.path import join, dirname, realpath

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # MONGO_URI = os.environ.get('MONGO_URI')
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    # DB_NAME = "development-db"
    # DB_USERNAME = "admin"
    # DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    # DB_NAME = "development-db"
    # DB_USERNAME = "admin"
    # DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False