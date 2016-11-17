#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import models
import math
from flask import request, url_for
# HORRIBLE HACK PARA IMPORTAR EL MODULO, ARREGLAR:
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir2 = os.path.dirname(parentdir)
sys.path.insert(0, parentdir2)
from text_classifier import TextClassifier
from datetime import datetime


class SpreadSheetReader:

    def __init__(self):
        pass

    @classmethod
    def first_read(cls, filename):
        extension = filename.split('.')[-1]
        with open('app/uploads/' + filename, 'rb') as spreadsheet_file:

            if extension == 'csv':
                spreadsheet = cls.read_csv(spreadsheet_file)

            # TODO: leer xls y xlsx

            summary = {'best_row': []}
            for i, row in spreadsheet:
                if i > 100:
                    break
                elif i == 0:
                    summary['first_row'] = row
                else:
                    summary['best_row'] = cls._best_row(summary['best_row'], row)
            if i == 0:
                summary['best_row'] = cls._best_row(summary['best_row'], row)
            return summary

    @classmethod
    def read_csv(cls, csvfile):
        dialect = csv.Sniffer().sniff(csvfile.read(10240), delimiters=';,')
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for i, row in enumerate(reader):
            yield (i, [unicode(cell, 'utf-8') for cell in row])

    @staticmethod
    def _best_row(first_row, second_row):

        def columns_with_values(row):
            return sum([1 for field in row if len(field.strip()) > 0])

        def average_column_length(row):
            return sum([len(field.strip()) for field in row]) / float(len(row))

        first_columns_with_values = columns_with_values(first_row)
        second_columns_with_values = columns_with_values(second_row)
        if first_columns_with_values > second_columns_with_values:
            return first_row
        elif second_columns_with_values > first_columns_with_values:
            return second_row
        else:
            first_average = average_column_length(first_row)
            second_average = average_column_length(second_row)
            if first_average > second_average:
                return first_row
            return second_row


class Searcher:

    def __init__(self):
        self.text_classifier = None
        self.restart_text_classifier()
        self.per_page = 10

    def restart_text_classifier(self):
        all_questions = models.Question.query.all()
        if len(all_questions) > 0:
            ids = [str(q.id) for q in all_questions]
            texts = [q.body + q.context for q in all_questions]
            try:
                self.text_classifier = TextClassifier(texts, ids)
                self.restart_suggesters(all_questions)
            except Exception as e:
                print e

    def restart_suggesters(self, questions):
        ids = [str(q.id) for q in questions]
        topics = [q.topic.name for q in questions]
        subtopics = [q.subtopic.name for q in questions]
        topics_ids = [str(q.topic_id) for q in questions]
        subtopic_ids = [str(q.subtopic_id) for q in questions]
        good_topics = [i for i, t in enumerate(topics) if len(t) > 2]
        ids_good_topics = [ids[i] for i in good_topics]
        good_topics_ids = [topics_ids[i] for i in good_topics]
        self.text_classifier.make_classifier(
            "topics", ids_good_topics, good_topics_ids)
        all_topics = models.Topic.query.all()
        for topic in all_topics:
            if len(topic.name) < 2:
                continue
            ids_within_topic = [ids[i] for i, t in enumerate(zip(topics, subtopics))
                                if t[0] == topic.name and len(t[1]) > 2]
            subtopic_ids_within_topic = [subtopic_ids[i] for i, t in enumerate(zip(topics, subtopics))
                                         if t[0] == topic.name and len(t[1]) > 2]
            if len(set(subtopic_ids_within_topic)) > 2:
                self.text_classifier.make_classifier(str(topic.id) + "_subtopics",
                                                     ids_within_topic,
                                                     subtopic_ids_within_topic)

    @staticmethod
    def list_models():
        return {
            u'Autor': models.Author.query.all(),
            u'Informe': models.Report.query.all(),
            u'Área de Gestión': models.SubTopic.query.all(),
            u'Ministerio': models.Topic.query.all(),
        }

    def get_question(self, question_id):
        question = models.Question.query.get(question_id)
        return question

    def search_from_url(self):
        query = self.query_from_url()
        return self.search(query)

    def delete_results_from_url(self, db_session):
        results = self.search_from_url()
        result_list = results['result_list']
        for question, keywords in result_list:
            db_session.delete(question)
        db_session.commit()
        return

    def search(self, query):
        if query['text'] is not None:
            results = self._search_similar(query['text'])
        else:
            results = models.Question.query.all()
            results = [(result, []) for result in results]
        results = self._filter_results(results, query['filters'])
        return self._paginate(results, query)

    def _paginate(self, results, query):
        pagination = {
            'current_page': query['current_page'],
            'total_pages': int(math.ceil(len(results) / float(self.per_page))),
            'total_results': len(results)
        }
        from_position = (pagination['current_page'] - 1) * self.per_page
        to_position = pagination['current_page'] * self.per_page
        return {
            'pagination': pagination,
            'result_list': results[from_position:to_position],
            'query': query
        }

    @staticmethod
    def _filt_fun(result, filter_ids):
        """Recives an item of the results list [(result, best_words)]
            and a dict of filter_ids and decides whether that element is
            accepted by the filter or not.
        """
        result_only = result[0]
        comparators = [True if len(v) > 0 and getattr(result_only, k) == v[0].id else False
                       for k, v in filter_ids.iteritems()]
        return all(comparators)

    def _filter_results(self, results, filters):
        filt_models = {'tema': ('topic_id', models.Topic),
                       'subtema': ('subtopic_id', models.SubTopic),
                       'autor': ('author_id', models.Author),
                       'informe': ('report_id', models.Report)}
        filt_ids = {v[0]: v[1].query.filter_by(name=filters[k]).all()
                    for k, v in filt_models.iteritems() if k in filters.keys()}
        filtered_questions = filter(lambda x: self._filt_fun(x, filt_ids), results)
        if 'creado-en' in filters:
            created_at = datetime.strptime(filters['creado-en'], '%Y-%m-%d %H:%M:%S')
            filtered_questions = filter(lambda x: x[0].created_at == created_at, filtered_questions)
        return filtered_questions

    def get_similar_to(self, question_id):
        query = self.query_from_url()
        query['text'] = question_id
        return self.search(query)

    def _search_similar(self, question_id):
        if self.text_classifier is None:
            return []
        if not isinstance(question_id, basestring):
            question_id = str(question_id)
        ids_sim, dist, best_words = self.text_classifier.get_similar(
            question_id, max_similars=self.per_page)
        ids_sim = map(int, ids_sim)
        results = []
        for qid in ids_sim:
            results.append(models.Question.query.get(qid))
        return zip(results, best_words)

    def suggest_tags(self, tag_type, question_id):
        question = models.Question.query.get(question_id)
        classifier_name = str(question.topic_id) + "_" + tag_type
        if classifier_name in dir(self.text_classifier):
            tags, vals = self.text_classifier.classify(classifier_name,
                                                       [str(question_id)])
            myModel = models.SubTopic
        elif 'subtopics' in tag_type:
            subtopics = question.topic.subtopics
            return list(sorted([x.name for x in subtopics]))
        elif tag_type == 'topics':
            tags, vals = self.text_classifier.classify('topics',
                                                       [str(question_id)])
            myModel = models.Topic
        tag_names = [myModel.query.get(idt).name for idt in tags]
        sorted_tags = [x for (y, x) in sorted(zip(vals.tolist()[0], tag_names))]
        return list(reversed(sorted_tags))

    def query_from_url(self):
        filter_titles = ['tema',
                         'subtema',
                         'autor',
                         'informe',
                         'organismo-requerido',
                         'pregunta',
                         'creado-en']
        return {
            'text': request.args.get('q'),
            'current_page': int(request.args.get('pagina', 1)),
            'can_add_more_filters': True,
            'filters': {t: request.args.get(t).lower() for t in filter_titles
                        if request.args.get(t) is not None},
        }

    def url_maker(self, query, page=None):
        args = {}
        if 'text' in query and query['text'] is not None:
            args['q'] = query['text']
        for title, value in query['filters'].iteritems():
            args[title] = value
        if page is not None:
            args['pagina'] = page
        return url_for('search', **args)
