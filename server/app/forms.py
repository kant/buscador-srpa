from flask.ext.wtf import Form
from wtforms import validators, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_user.translations import lazy_gettext as _
from models import MAX_TEXT_LENGTH, Question
from werkzeug.utils import secure_filename


class QuestionForm(Form):
    number = IntegerField(
        _('Question number'),
        [validators.NumberRange(min=1, message=_('Question number must be a positive integer'))]
    )
    body = TextAreaField(
        _('Question body'),
        [validators.Length(min=1, max=MAX_TEXT_LENGTH)]
    )
    justification = TextAreaField(
        _('Question justification (optional)'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )
    context = TextAreaField(
        _('Question context (optional)'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )

    def save_question(self, db_session):
        question = Question(
            number=self.number.data,
            body=self.body.data,
            justification=self.justification.data,
            context=self.context.data
        )
        db_session.add(question)
        db_session.commit()


class UploadForm(Form):
    spreadsheet = FileField(
        'spreadsheet',
        validators=[FileRequired(), FileAllowed(['xls', 'xlsx', 'csv'], 'Spreadsheets only (.xsl, .xslx, .csv)')]
    )

    def save_spreadsheet(self):
        filename = secure_filename(self.spreadsheet.data.filename)
        self.spreadsheet.data.save('app/uploads/' + filename)
