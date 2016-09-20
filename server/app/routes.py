from flask import render_template
from flask_user import login_required


def init_routes(app):
    @app.route('/')
    @login_required
    def home_page():
        return render_template('home.html')