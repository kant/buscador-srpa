class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    USER_APP_NAME = "PreguntasJGM"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'

    MAIL_USERNAME = 'noreply@jgm.com'
    MAIL_DEFAULT_SENDER = 'no-reply <noreply@jgm.com>'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = False

# class ProductionConfig(Config):
#    DATABASE_URI = 'mysql://user@localhost/foo'
