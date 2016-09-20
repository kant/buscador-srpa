from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager
from . import app, db, models
from routes import init_routes


def create_app():
    app.config.from_object('app.config.DevelopmentConfig')
    Mail(app)
    db.create_all()
    db_adapter = SQLAlchemyAdapter(db, models.User)
    UserManager(db_adapter, app)
    init_routes(app)
    return app
