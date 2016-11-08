#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import validators, IntegerField, TextAreaField, BooleanField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_user.translations import lazy_gettext as _
from models import MAX_TEXT_LENGTH, Question, Report, Topic, SubTopic, Author, get_or_create
import time
from helpers import SpreadSheetReader
from flask import render_template, redirect, url_for


class QuestionForm(Form):
    number = IntegerField(
        _('Question number'),
        [validators.NumberRange(min=1, message=_('Question number must be a \
                                                  positive integer'))]
    )
    body = TextAreaField(
        _('Question body'),
        [validators.Length(min=1, max=MAX_TEXT_LENGTH)]
    )
    context = TextAreaField(
        _('Question context (optional)'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )
    report = TextAreaField(
        _('Report number'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )
    author = TextAreaField(
        _('Question author'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )
    topic = TextAreaField(
        _('Question topic'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )
    subtopic = TextAreaField(
        _('Question subtopic'),
        [validators.Length(min=0, max=MAX_TEXT_LENGTH)]
    )

    def populate_question(self, question):
        self.number.data = question.number
        self.body.data = question.body
        self.context.data = question.context
        self.report.data = question.report.name
        self.author.data = question.author.name
        self.topic.data = question.topic.name
        self.subtopic.data = question.subtopic.name

    def save_question(self, db_session):
        report_id = get_or_create(
            db_session, Report, name=self.report.data.strip().lower())
        author_id = get_or_create(
            db_session, Author, name=self.author.data.strip().lower())
        topic_id = get_or_create(
            db_session, Topic, name=self.topic.data.strip().lower())
        subtopic_id = get_or_create(
            db_session, SubTopic, name=self.subtopic.data.strip().lower())
        mytopic = Topic.query.get(topic_id)
        mysubtopic = SubTopic.query.get(subtopic_id)
        mytopic.subtopics.append(mysubtopic)

        question = Question(
            number=self.number.data,
            body=self.body.data.strip(),
            context=self.context.data.strip(),
            report_id=report_id,
            author_id=author_id,
            topic_id=topic_id,
            subtopic_id=subtopic_id
        )
        db_session.add(question)
        db_session.commit()
        return question

    def update_question(self, question, db_session):
        question.number = self.number.data
        question.body = self.body.data.strip()
        question.context = self.context.data.strip()
        question.report_id = get_or_create(db_session, Report, name=self.report.data.strip().lower())
        question.author_id = get_or_create(db_session, Author, name=self.author.data.strip().lower())
        question.topic_id = get_or_create(db_session, Topic, name=self.topic.data.strip().lower())
        question.subtopic_id = get_or_create(db_session, SubTopic, name=self.subtopic.data.strip().lower())
        db_session.add(question)
        db_session.commit()

    def handle_create_request(self, db_session, searcher):
        if self.validate_on_submit():
            question = self.save_question(db_session)
            searcher.restart_text_classifier()
            return redirect(url_for('see_question', question_id=question.id))
        return render_template('forms/single_question_form.html', form=self)

    def handle_edit_request(self, request, db_session, searcher, question_id):
        question = searcher.get_question(question_id)
        if self.validate_on_submit():
            self.update_question(question, db_session)
            searcher.restart_text_classifier()
            return redirect(url_for('see_question', question_id=question.id))
        self.populate_question(question)
        standalone = request.args.get('standalone', False)
        return render_template('forms/single_question_form.html',
                               form=self, question=question, standalone=standalone)


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

    def handle_request(self):
        if self.validate_on_submit():
            filename = self.save_spreadsheet()
            return redirect(url_for('process_spreadsheet', filename=filename))
        return render_template('forms/question_upload_form.html', form=self)


class ProcessSpreadsheetForm(Form):
    discard_first_row = BooleanField(_('First row is header'), default=True)
    number = SelectField(_('Question number'), [validators.DataRequired("Requerido")])
    body = SelectField(_('Question body'), [validators.DataRequired("Requerido")])
    context = SelectField(_('Question context'))
    report = SelectField(_('Report number'))
    author = SelectField(_('Question author'))
    topic = SelectField(_('Question topic'))
    subtopic = SelectField(_('Question subtopic'))

    def handle_request(self, filename, db_session, searcher):
        spreadsheet_summary = SpreadSheetReader.first_read(filename)
        self.update_choices(spreadsheet_summary['first_row'])
        if self.validate_on_submit():
            self.save_models(filename, db_session)
            searcher.restart_text_classifier()
            return redirect(url_for('search'))
        else:
            print(self.errors)
        return render_template(
            'forms/process_spreadsheet.html',
            filename=filename,
            spreadsheet_summary=spreadsheet_summary,
            form=self
        )

    def update_choices(self, first_row):
        choices = [(str(i), first_row[i]) for i in range(len(first_row))]
        choices = [('', _('None'))] + choices
        self.number.choices = choices
        self.body.choices = choices
        self.context.choices = choices
        self.report.choices = choices
        self.author.choices = choices
        self.topic.choices = choices
        self.subtopic.choices = choices

    def save_models(self, filename, db_session):
        columns = self._collect_columns()
        extension = filename.split('.')[-1]
        with open('app/uploads/' + filename, 'rb') as spreadsheet_file:

            if extension == 'csv':
                spreadsheet = SpreadSheetReader.read_csv(spreadsheet_file)
            # TODO: leer xls y xlsx

            for i, row in spreadsheet:
                if i == 0 and self.discard_first_row.data:
                    continue
                args = self.collect_args(row, columns)
                args = self._get_ids(args, db_session)
                question = Question(**args)
                db_session.add(question)
            db_session.commit()

    def _collect_columns(self):
        columns = [
            (self.number.data, 'number'),
            (self.body.data, 'body'),
            (self.context.data, 'context'),
            (self.report.data, 'report'),
            (self.author.data, 'author'),
            (self.topic.data, 'topic'),
            (self.subtopic.data, 'subtopic')
        ]
        return [(int(tuple[0]), tuple[1]) for tuple in columns
                if len(tuple[0]) > 0]

    def _get_ids(self, question_args, db_session):
        if 'report' in question_args.keys():
            question_args['report_id'] = get_or_create(
                db_session, Report, name=question_args['report'])
        if 'author' in question_args.keys():
            question_args['author_id'] = get_or_create(
                db_session, Author, name=question_args['author'])
        if 'topic' in question_args.keys():
            question_args['topic_id'] = get_or_create(
                db_session, Topic, name=question_args['topic'])
        if 'subtopic' in question_args.keys():
            question_args['subtopic_id'] = get_or_create(
                db_session, SubTopic, name=question_args['subtopic'])
            mytopic = Topic.query.get(question_args['topic_id'])
            mysubtopic = SubTopic.query.get(question_args['subtopic_id'])
            mytopic.subtopics.append(mysubtopic)
            db_session.commit()
        return question_args

    @staticmethod
    def collect_args(row, columns):
        d = {}
        for col in columns:
            position = col[0]
            if 0 <= position < len(row):
                value = row[col[0]].strip()
                if col[1] in ['author', 'report', 'topic', 'subtopic']:
                    value = value.lower()
            else:
                value = ''
            d[col[1]] = value
        return d


class FullTextQueryForm(Form):
    main_text = TextAreaField(
        _('Base text to query'),
        [validators.Length(min=1, max=2000)]
    )

    def handle_request(self):
        if self.validate_on_submit():
            return redirect(url_for('search', q=self.main_text.data))
        return render_template('forms/full_text_query.html', form=self)
