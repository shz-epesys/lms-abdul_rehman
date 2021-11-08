import os
from dotenv import dotenv_values

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = '.env'
dotenv_values(dotenv_path)

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.environ['USERNAME'],
    os.environ['PASSWORD'],
    os.environ['HOST'],
    os.environ['DATABASE'],
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
