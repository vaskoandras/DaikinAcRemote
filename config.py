import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = os.environ.get('DEBUG')
    DRY_RUN = os.environ.get('DRY_RUN', False)

    DATABASE = {
        'name': os.environ.get('DB_DB'),
        'host': os.environ.get('DB_HOST'),
        'engine': 'peewee.MySQLDatabase',
        'user': os.environ.get('DB_USERNAME'),
        'passwd': os.environ.get('DB_PASSWORD'),
    }