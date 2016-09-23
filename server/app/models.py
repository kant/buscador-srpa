from . import db
from flask_user import UserMixin


# TODO: chequear longitudes de los campos de texto


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


class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(1000), nullable=False, server_default='')
    justification = db.Column(db.Text(1000), nullable=False, server_default='')
    context = db.Column(db.Text(1000), nullable=False, server_default='')
    answerers = db.relationship('Answerer', secondary='question_answerers', backref=db.backref('questions', lazy='dynamic'))
    keywords = db.relationship('Keyword', secondary='question_keywords', backref=db.backref('questions', lazy='dynamic'))
    report_id = db.Column(db.Integer(), db.ForeignKey('report.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('author.id'))
    topic_id = db.Column(db.Integer(), db.ForeignKey('topic.id'))
    subtopic_id = db.Column(db.Integer(), db.ForeignKey('sub_topic.id'))


class Keyword(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)


class QuestionKeywords(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id'))
    keyword_id = db.Column(db.Integer(), db.ForeignKey('keyword.id'))


class Report(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    questions = db.relationship('Question', backref='report')


class Topic(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    questions = db.relationship('Question', backref='topic')
    subtopics = db.relationship('SubTopic', backref='topic')


class SubTopic(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    questions = db.relationship('Question', backref='subtopic')
    topic_id = db.Column(db.Integer(), db.ForeignKey('topic.id'))


class Author(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    questions = db.relationship('Question', backref='author')
    # TODO: agregar origen del autor (prov, ciudad, etc)
    # y bloque al cual pertenece (ver excel)


class Answerer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)


class QuestionAnswerers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id'))
    answerer_id = db.Column(db.Integer(), db.ForeignKey('answerer.id'))


# class RelatedQuestions(db.Model):
#     pass
#
#
# class Answer(db.Model):
#     pass
