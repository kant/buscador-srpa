from flask import render_template, request, redirect
from flask_user import login_required
from forms import QuestionForm, UploadForm


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
            return redirect('/carga_de_preguntas/interpretar_planilla', filename=filename)
        return render_template('forms/question_upload_form.html', upload_form=upload_form)

    @login_required
    @app.route('/carga_de_preguntas/manual', methods=['GET', 'POST'])
    def single_question():
        single_question_form = QuestionForm()
        if single_question_form.validate_on_submit():
            single_question_form.save_question(db_session)
            return redirect('/')
        return render_template('forms/single_question_form.html', question_form=single_question_form)

    @login_required
    @app.route('/busqueda_por_similaridad', methods=['GET', 'POST'])
    def full_text_query():
        return render_template('full_text_query.html')

    @login_required
    @app.route('/buscar', methods=['GET', 'POST'])
    def search():
        return render_template('search.html')

    @login_required
    @app.route('/gestion_de_entidades')
    def management():
        return render_template('management.html')
