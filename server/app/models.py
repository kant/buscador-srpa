from . import db
from flask_user import UserMixin


# TODO: chequear longitudes de los campos de texto
MAX_TEXT_LENGTH = 1000
MAX_NAME_LENGTH = 255


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    password = db.Column(db.String(255), nullable=False)
    reset_password_token = db.Column(db.String(100))
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.active = kwargs.get('active', False)
        self.password = kwargs.get('password', None)
        self.email = kwargs.get('email', None)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    number = db.Column(db.Integer)
    body = db.Column(db.Text(MAX_TEXT_LENGTH))
    justification = db.Column(db.Text(MAX_TEXT_LENGTH))
    context = db.Column(db.Text(MAX_TEXT_LENGTH))
    answerers = db.relationship('Answerer', secondary='question_answerers', backref=db.backref('questions', lazy='dynamic'))
    keywords = db.relationship('Keyword', secondary='question_keywords', backref=db.backref('questions', lazy='dynamic'))
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    subtopic_id = db.Column(db.Integer, db.ForeignKey('sub_topic.id'))

    def __init__(self, **kwargs):
        self.number = kwargs.get('number', None)
        self.body = kwargs.get('body', '')
        self.justification = kwargs.get('justification', '')
        self.context = kwargs.get('context', '')
        self.answerers = kwargs.get('answerers', [])
        self.keywords = kwargs.get('keywords', [])
        self.report_id = kwargs.get('report_id', None)
        self.author_id = kwargs.get('author_id', None)
        self.topic_id = kwargs.get('topic_id', None)
        self.subtopic_id = kwargs.get('subtopic_id', None)

    @classmethod
    def delete(cls, question_id, db_session):
        question = cls.query.get(question_id)
        db_session.delete(question)
        db_session.commit()


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)


class QuestionKeywords(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'))


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)
    date = db.Column(db.Date())
    questions = db.relationship('Question', backref='report')


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)
    questions = db.relationship('Question', backref='topic')
    subtopics = db.relationship('SubTopic', backref='topic')


class SubTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)
    questions = db.relationship('Question', backref='subtopic')
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)
    questions = db.relationship('Question', backref='author')
    # TODO: agregar origen del autor (prov, ciudad, etc)
    # y bloque al cual pertenece (ver excel)


class Answerer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), unique=True)


class QuestionAnswerers(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answerer_id = db.Column(db.Integer, db.ForeignKey('answerer.id'))


# class RelatedQuestions(db.Model):
#     pass
#
#
# class Answer(db.Model):
#     pass
