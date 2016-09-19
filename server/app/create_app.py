from flask import Flask, render_template_string, request
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask_user import roles_required
from app import app, db, models

def create_app():
  app.config.from_pyfile('config.py')
  db.create_all()

  # Setup Flask-User
  db_adapter = SQLAlchemyAdapter(db, models.User)
  user_manager = UserManager(db_adapter, app)

  # Create 'user007' user with 'secret' and 'agent' roles
  if not models.User.query.filter(models.User.username=='user007').first():
    user1 = models.User(username='user007', email='user007@example.com', active=True, password=user_manager.hash_password('Password1'))
    user1.roles.append(models.Role(name='secret'))
    user1.roles.append(models.Role(name='agent'))
    db.session.add(user1)
    db.session.commit()

  # The Home page is accessible to anyone
  @app.route('/')
  def home_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Home page</h2>
            <p>This page can be accessed by anyone.</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
        {% endblock %}
        """)

  # The Members page is only accessible to authenticated users
  @app.route('/members')
  @login_required                                 # Use of @login_required decorator
  def members_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Members page</h2>
            <p>This page can only be accessed by authenticated users.</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
        {% endblock %}
        """)

  # The Special page requires a user with 'special' and 'sauce' roles or with 'special' and 'agent' roles.
  @app.route('/special')
  @roles_required('secret', ['sauce', 'agent'])   # Use of @roles_required decorator
  def special_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Special Page</h2>
            <p>This page can only be accessed by user007.</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
        {% endblock %}
        """)

  return app