import os

SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')
CSRF_ENABLED = False

MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'email@example.com')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'password')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')
MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
MAIL_PORT = int(os.getenv('MAIL_PORT', '25'))
MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', False))

USER_APP_NAME = "PreguntasJGM"
