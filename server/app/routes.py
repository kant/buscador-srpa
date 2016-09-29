from flask import render_template, request, redirect, url_for
from flask_user import login_required
from forms import QuestionForm, UploadForm, ProcessSpreadsheetForm, FullTextQueryForm
from helpers import SpreadSheetReader


def init_routes(app, db_session):
    @app.route('/')
    @login_required
    def home_page():
        return render_template('home.html')

    @app.route('/carga_de_preguntas', methods=['GET', 'POST'])
    @login_required
    def question_upload():
        upload_form = UploadForm()
        if upload_form.validate_on_submit():
            filename = upload_form.save_spreadsheet()
            return redirect(url_for('process_spreadsheet', filename=filename))
        return render_template('forms/question_upload_form.html', upload_form=upload_form)

    @app.route('/carga_de_preguntas/manual', methods=['GET', 'POST'])
    @login_required
    def single_question():
        single_question_form = QuestionForm()
        if single_question_form.validate_on_submit():
            single_question_form.save_question(db_session)
            return redirect(url_for('home_page'))
        return render_template('forms/single_question_form.html', question_form=single_question_form)

    @app.route('/carga_de_preguntas/procesar_planilla/<filename>')
    @login_required
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

    @app.route('/busqueda_por_similaridad', methods=['GET', 'POST'])
    @login_required
    def full_text_query():
        form = FullTextQueryForm()
        return render_template('forms/full_text_query.html', form=form)

    @app.route('/buscar', methods=['GET', 'POST'])
    @login_required
    def search():
        return render_template('search.html')

    @app.route('/gestion_de_entidades')
    @login_required
    def management():
        return render_template('management.html')
