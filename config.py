
import os
from dotenv import load_dotenv
from flask.app import Flask

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mars:Mars12345@localhost/lms'

SQLALCHEMY_TRACK_MODIFICATIONS = False
dotenv_path = '.env'
load_dotenv(dotenv_path)
