from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager
from flask.ext.babel import Babel
from . import app, db, models
from routes import init_routes
from helpers import Searcher

def create_db():
    app.config.from_object('app.config.Config')
    db.create_all()

def create_app():
    create_db()
    Babel(app)
    Mail(app)
    init_users()
    searcher = Searcher()
    init_routes(app, db.session, searcher)
    return app

def init_users():
    db_adapter = SQLAlchemyAdapter(db, models.User)
    user_manager = UserManager(db_adapter, app)
    if not models.User.query.filter(models.User.email == 'admin@modernizacion.gob.ar').first():
        admin_user = models.User(
            email='admin@modernizacion.gob.ar',
            active=True,
            password=user_manager.hash_password('Modernizacion')
        )
        db.session.add(admin_user)
        db.session.commit()
    return
