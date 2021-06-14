import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir + "/../", "db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = 0
SECRET_KEY = 'secret-key'
JWT_TOKEN_TIMEOUT = timedelta(days=2)
