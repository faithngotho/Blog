import os

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = "1234"
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLCLCHEMY_RECORD_QUERIES = True
    CSRF_ENABLED = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.gmail.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','faithwangari248@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','34816809')
    MAIL_SENDER = os.environ.get('MAIL_SENDER', 'Project Admin<faithwangari248@gmail.com>')
    PROJECT_ADMIN = os.environ.get('PROJECT_ADMIN', 'PROJECT_ADMIN')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SUBJECT_PREFIX = '[PROJECT]'

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):
    '''
    Production configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') 

class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://faith:34816809@localhost/blog'

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}
