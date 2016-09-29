from flask import render_template, request, flash, redirect
from flask_user import login_required
from forms import QuestionForm
from models import Question


def init_routes(app, db_session):
    @app.route('/')
    def home_page():
        return render_template('home.html')

    @login_required
    @app.route('/carga', methods=['GET', 'POST'])
    def question_form():
        form = QuestionForm(request.form)
        if request.method == 'POST' and form.validate():
            question = Question(
                number=form.number.data,
                body=form.body.data,
                justification=form.justification.data,
                context=form.context.data
            )
            db_session.add(question)
            db_session.commit()
            return redirect('/')
        return render_template('forms/question_form.html', form=form)

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
