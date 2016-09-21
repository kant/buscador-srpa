from . import db
from flask_user import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

#
# class Question(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#
#
# class RelatedQuestions(db.Model):
#     pass
#
#
# class Keyword(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), unique=True)
#
#
# class QuestionKeywords(db.Model):
#     pass
#
#
# class Answer(db.Model):
#     pass
#
#
# class Report(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     date = db.Column(db.Date())
#
#
# class Tag(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), unique=True)
#
#
# class Author(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), unique=True)
#
#
# class Answerer(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(200), unique=True)
#
#
# class QuestionAnswerers(db.Model):
#     pass
