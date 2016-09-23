from wtforms import Form, validators, IntegerField, TextAreaField
from flask_user.translations import lazy_gettext as _
from models import MAX_TEXT_LENGTH


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
