from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager
from flask.ext.babel import Babel
from . import app, db, models
from routes import init_routes
from helpers import Searcher
# HORRIBLE HACK PARA IMPORTAR EL MODULO, ARREGLAR:
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0, parentdir2)
from text_classifier import TextClassifier


def create_app():
    app.config.from_object('app.config.DevelopmentConfig')
    Babel(app)
    Mail(app)
    db.create_all()
    init_users()
    text_classifier = init_text_classifier()
    searcher = Searcher(text_classifier)
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


def init_text_classifier():
    all_questions = models.Question.query.all()
    ids = [str(q.id) for q in all_questions]
    texts = [q.body for q in all_questions]
    return TextClassifier(texts, ids)
