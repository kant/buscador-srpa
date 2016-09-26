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
