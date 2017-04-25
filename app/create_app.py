from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager
from flask.ext.babel import Babel
from . import app, db, models
from routes import init_routes
from helpers import Searcher
import getpass
import os

def create_db():
    app.config.from_object('app.config.Config')
    db.create_all()


def create_app():
    create_db()
    Babel(app)
    Mail(app)
    db_adapter = SQLAlchemyAdapter(db, models.User)
    UserManager(db_adapter, app)
    searcher = Searcher()
    init_routes(app, db.session, searcher)
    return app


def create_user():
    os.environ['SMTP_PASS'] = os.environ.get('SMTP_PASS', '')
    app.config.from_object('app.config.Config')
    db_adapter = SQLAlchemyAdapter(db, models.User)
    user_manager = UserManager(db_adapter, app)
    email = raw_input("User email: ")
    if not models.User.query.filter(models.User.email == email).first():
        password = getpass.getpass('User password: ')
        password2 = getpass.getpass('Confirm user password: ')
        if password == password2:
            admin_user = models.User(
                email=email,
                active=True,
                password=user_manager.hash_password(password)
            )
            db.session.add(admin_user)
            db.session.commit()
            print('User created successfully')
        else:
            print("The passwords don't match")
    else:
        print('The user already exists')
    return
