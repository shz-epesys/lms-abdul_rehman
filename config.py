import os
from dotenv import dotenv_values

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = '.env'
dotenv_values(dotenv_path)

SECRET_KEY = os.environ['SECRET_KEY']
UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.environ['USERNAME'],
    os.environ['PASSWORD'],
    os.environ['HOST'],
    os.environ['DATABASE'],
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
