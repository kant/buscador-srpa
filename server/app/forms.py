from flask.ext.wtf import Form
from wtforms import validators, IntegerField, TextAreaField, BooleanField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_user.translations import lazy_gettext as _
from models import MAX_TEXT_LENGTH, Question
import time


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
        original_filename = self.spreadsheet.data.filename
        new_filename = str(int(time.time())) + '.' + original_filename.split('.')[-1]
        self.spreadsheet.data.save('app/uploads/' + new_filename)
        return new_filename


class ProcessSpreadsheetForm(Form):
    discard_first_row = BooleanField(_('First row is header'), [validators.DataRequired()])
    number = SelectField('Question number')
    body = SelectField('Question body')
    justification = SelectField('Question justification')
    context = SelectField('Question context')

    def update_choices(self, spreadsheet_summary):
        first_row = spreadsheet_summary['first_row']
        choices = [(str(i), first_row[i]) for i in range(len(first_row))]
        self.number.choices = choices
        self.body.choices = choices
        self.justification.choices = choices
        self.context.choices = choices
