from flask import render_template
from flask_user import login_required


def init_routes(app):
    @app.route('/')
    def home_page():
        return render_template('home.html')