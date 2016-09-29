# coding: utf-8
from flask import render_template, request, redirect, url_for
from flask_user import login_required
from forms import QuestionForm, UploadForm, ProcessSpreadsheetForm, FullTextQueryForm
from helpers import SpreadSheetReader
from datetime import date


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
        result_list = fake_results()
        query = {
            'text': u'¿Existen exenciones impositivas a nivel nacional para los sectores sociales damnificados por las inundaciones en Entre Rios?',
            'can_add_more_filters': True,
            'filters': [

            ]
        }
        return render_template('search/results.html', result_list=result_list, query=query)

    @app.route('/pregunta')
    @login_required
    def see_question():
        return render_template('question.html')

    @app.route('/gestion_de_entidades')
    @login_required
    def management():
        return render_template('management.html')

    def fake_results():
        return [{
            'report': {
                'date': date(2015, 12, 31)
            },
            'body': u'Venta de aviones pertenecientes a la flota presidencial ¿Cuáles fueron los criterios para determinar la venta de la flota de aviones? Respecto de la recaudación de dicha venta: indique con qué fines serán utilizados dichos fondos. ¿Se ha realizado un relevamiento sobre el actual estado de los aviones para colocarlos en venta? ¿Existe otra autoridad encargada de auditar la transparencia de dichas operaciones?',
            'author': {
                'name': u'Bloque Compromiso Federal'
            },
            'answerer': {
                'name': u'Secretaría General de la Presidencia'
            },
            'topic': u'Transporte',
            'subtopic': u'Otros',
            'context': u''
        }, {
            'report': {
                'date': date(2016, 5, 22)
            },
            'body': u'¿Por qué el Ministerio de trabajo y su gobierno no responden al reclamo de los trabajadores contra los despidos?',
            'author': {
                'name': u'Bloque Frente de Izquierda y de los Trabajadores'
            },
            'answerer': {
                'name': u'Ministerio de Trabajo, Empleo y Seguridad Social'
            },
            'topic': u'Empleo',
            'subtopic': u'Política de Empleo y Desempleo',
            'context': u'Han habido importantes huelgas y movilizaciones, como la reciente del Comodorazo, contra la política de parate de la industria petrolera y en defensa de los puestos de trabajo'
        }, {
            'report': {
                'date': date(2015, 4, 28)
            },
            'body': u'Informe sobre montos abonados y devengados en concepto de indemnizaciones, preaviso y toda otra suma derivada del distracto laboral en los casos previstos en la pregunta anterior.',
            'author': {
                'name': u'Bloque Justicialista'
            },
            'answerer': {
                'name': u'Ministerio de Trabajo, Empleo y Seguridad Social'
            },
            'topic': u'Empleo ',
            'subtopic': u'ANSES',
            'context': u'Sobre los despidos en la UDAI Mercedes, provincia de Corrientes de la Administración Nacional de la Seguridad Social (ANSES), producidos entre el 11 de Diciembre de 2015 y el 01 de Junio de 2016.'
        }, {
            'report': {
                'date': date(2015, 7, 5)
            },
            'body': u'Cuáles son los motivos por los cuales aquellas víctimas del Terrorismo de Estado, que cumplen todos los requisitos establecidos el Art. 1° de la mencionada ley, no están recibiendo la indemnización correspondiente. ',
            'author': {
                'name': u'Bloque Proyecto Sur'
            },
            'answerer': {
                'name': u'Ministerio de Justicia y Derechos Humanos'
            },
            'topic': u'Justicia',
            'subtopic': u'Otros',
            'context': u'En relación con las leyes de reparación a las víctimas del Terrorismo de Estado, en particular del Régimen Reparatorio de la ley N° 26.913, para los ex presos políticos en la República Argentina durante la última dictadura cívico-militar, explique:'
        }, {
            'report': {
                'date': date(2016, 5, 12)
            },
            'body': u'Informe las razones por las cuáles el Gobierno argentino se pone en primera fila a nivel internacional para legitimar el golpe institucional en Brasil y recibe y hasta firma “acuerdos de entendimiento para el establecimiento de mecanismos bilaterales de coordinación política” a través de la canciller Susana Malcorra con funcionarios de un gobierno nacido de un golpe institucional como el de Temer.',
            'author': {
                'name': u'Bloque PTS- Frente de Izquierda'
            },
            'answerer': {
                'name': u'Ministerio de Relaciones Exteriores y Culto'
            },
            'topic': u'Relaciones Exteriores',
            'subtopic': u'Integración regional',
            'context': u'Ya hemos requerido sin éxito precisiones al Jefe de Gabinete de Ministros en ocasión de su anterior visita a la Cámara de Diputados sobre la posición oficial del Gobierno nacional en relación al golpe institucional que se está consumando en Brasil. A su vez, el bloque PRO-Cambiemos de la Cámara de Diputados ya hizo de defensor del golpe institucional frente a las mociones que presentamos el 27 de abril y el 18 de mayo para repudiarlo; se negaron a tratarlo siquiera, mientras que 140 diputados votamos por hacerlo.  Luego de eso, el Poder Ejecutivo fue más allá en su reconocimiento al gobierno golpista de Michel Temer, al recibir al canciller José Serra con los brazos abiertos para dar apoyo directo al Gobierno golpista.'
        }, {
            'report': {
                'date': date(2015, 3, 22)
            },
            'body': u'¿Cuánto es en términos anuales el impacto de ese aumento del gas natural en el costo medio de generación en el mercado mayorista eléctrico?.',
            'author': {
                'name': u'Interbloque Federal Unidos por una Nueva Argentina'
            },
            'answerer': {
                'name': u'Ministerio de Energía y Minería'
            },
            'topic': u'Energía',
            'subtopic': u'Gas  ',
            'context': u'El costo de gas para la generación de energía eléctrica pasó del orden de los U$S 2,8 el millón de BTU a U$S 5 el millón de BTU, por lo que se sabe hasta ahora ese incremento sería cubierto por subsidios estatales ante el compromiso del gobierno de no volver a modificar las tarifas eléctricas para este año. '
        }]