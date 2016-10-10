#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request
from flask_user import login_required
from forms import QuestionForm, UploadForm, ProcessSpreadsheetForm, FullTextQueryForm


def init_routes(app, db_session, searcher):
    @app.route('/')
    @login_required
    def home_page():
        return render_template('home.html')

    @app.route('/carga_de_preguntas', methods=['GET', 'POST'])
    @login_required
    def question_upload():
        upload_form = UploadForm()
        return upload_form.handle_request()

    @app.route('/carga_de_preguntas/manual', methods=['GET', 'POST'])
    @login_required
    def single_question():
        single_question_form = QuestionForm()
        return single_question_form.handle_request(db_session)

    @app.route('/carga_de_preguntas/procesar_planilla/<filename>', methods=['GET', 'POST'])
    @login_required
    def process_spreadsheet(filename):
        process_spreadsheet_form = ProcessSpreadsheetForm()
        return process_spreadsheet_form.handle_request(filename, db_session, searcher)

    @app.route('/busqueda_por_similaridad', methods=['GET', 'POST'])
    @login_required
    def full_text_query():
        full_text_query_form = FullTextQueryForm()
        return full_text_query_form.handle_request()

    @app.route('/buscar', methods=['GET', 'POST'])
    @login_required
    def search():
        query = searcher.query_from_url()
        result_list = searcher.search_from_url()
        return render_template('search/results.html', result_list=result_list, query=query)

    @app.route('/pregunta/<int:question_id>')
    @login_required
    def see_question(question_id):
        question, similar_questions = searcher.get_question_and_similars(question_id)
        return render_template('question.html', question=question, similar_questions=similar_questions)

    @app.route('/gestion_de_entidades')
    @login_required
    def management():
        return render_template('management.html')
