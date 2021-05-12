import os
from os.path import join, dirname, realpath

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    SITE_DOCS = join(dirname(realpath(__file__)),"app/site_data/site_docs/")
    EMAIL_ID = os.environ.get('EMAIL_ID')
    EMAIL_PW = os.environ.get('EMAIL_PW')
    ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    PHONE_NUM = os.environ.get('PHONE_NUM')
    APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
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