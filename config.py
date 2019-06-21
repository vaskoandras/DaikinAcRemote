import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = os.environ.get('DEBUG')
    DRY_RUN = os.environ.get('DRY_RUN', False)

    DB_HOST = os.environ.get('DB_HOST')
    DB_DB = os.environ.get('DB_DB')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
