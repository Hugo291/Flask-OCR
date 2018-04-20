import os

FLASK_APP = '__init__.py'

# FLASK
DEBUG = True

STATIC_FOLDER = '/static'

# UPLOAD FILE SETTINGS

ALLOW_EXTENSION_FILE_UPLOAD = 'Pdf'

CURRENT_DIR = os.getcwd()

PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR))
CURRENT_DIR = os.getcwd()

UPLOAD_DIR_NAME = "upload"
UPLOAD_DIR_NAME = os.path.join('app', UPLOAD_DIR_NAME)

UPLOAD_DIR = os.path.join(PARENT_DIR, UPLOAD_DIR_NAME)

UPLOAD_DIR_PDF = os.path.join(UPLOAD_DIR, "pdf")
UPLOAD_DIR_JPG = os.path.join(UPLOAD_DIR, "jpg")
UPLOAD_DIR_TXT = os.path.join(UPLOAD_DIR, "txt")

MAX_CONTENT_LENGTH = 1000 * 1024 * 1024

UPLOAD_DIR_PDF_FILE = os.path.join(UPLOAD_DIR_PDF, 'file')
UPLOAD_DIR_PDF_PAGES = os.path.join(UPLOAD_DIR_PDF, 'pages')

# FLASK LOGIN SETTINGS
SECRET_KEY = 'secret_xxx'

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/descartes_mexique'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a SQLAlchemy Warning


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    pass


class TestConfig(Config):
    pass
