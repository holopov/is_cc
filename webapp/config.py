from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DOCUMENTS = os.path.join(basedir, 'static', 'documents')
REMEMBER_COOKIE_DURATION = timedelta(days=1)
SECRET_KEY = 'TOP_SECRET_KEY'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'base_app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

VERSION = '0.0.1'
ORGANIZATION = 'Наименование организации'
