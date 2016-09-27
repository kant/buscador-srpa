from flask import render_template, request, redirect, url_for
from flask_user import login_required
from forms import QuestionForm, UploadForm, ProcessSpreadsheetForm
from helpers import SpreadSheetReader


def init_routes(app, db_session):
    @app.route('/')
    def home_page():
        return render_template('home.html')

    @login_required
    @app.route('/carga_de_preguntas', methods=['GET', 'POST'])
    def question_upload():
        upload_form = UploadForm()
        if upload_form.validate_on_submit():
            filename = upload_form.save_spreadsheet()
            return redirect(url_for('process_spreadsheet', filename=filename))
        return render_template('forms/question_upload_form.html', upload_form=upload_form)

    @login_required
    @app.route('/carga_de_preguntas/manual', methods=['GET', 'POST'])
    def single_question():
        single_question_form = QuestionForm()
        if single_question_form.validate_on_submit():
            single_question_form.save_question(db_session)
            return redirect(url_for('home_page'))
        return render_template('forms/single_question_form.html', question_form=single_question_form)

    @login_required
    @app.route('/carga_de_preguntas/procesar_planilla/<filename>')
    def process_spreadsheet(filename):
        spreadsheet_summary = SpreadSheetReader.first_read(filename)
        process_spreadsheet_form = ProcessSpreadsheetForm()
        if process_spreadsheet_form.validate_on_submit():
            # procesar y guardar preguntas nuevas
            return redirect(url_for('home_page'))
        return render_template(
            'forms/process_spreadsheet.html',
            filename=filename,
            spreadsheet_summary=spreadsheet_summary,
            process_spreadsheet_form=process_spreadsheet_form
        )
