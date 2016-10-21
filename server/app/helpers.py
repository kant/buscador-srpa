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
            texts = [q.body for q in all_questions]
            topics_ids = [str(q.topic_id) for q in all_questions]
            subtopics_ids = [str(q.subtopic_id) for q in all_questions]
            ids_filt_topics = [ids[i] for i, x in enumerate(topics_ids)
                               if x != '1']
            ids_filt_subtopics = [ids[i] for i, x in enumerate(subtopics_ids)
                                  if x != '1']
            filtered_topics = filter(lambda x: x != '1', topics_ids)
            filtered_subtopics = filter(lambda x: x != '1', subtopics_ids)
            print("Entrenando con {:d}".format(len(ids_filt_topics)))
            try:
                self.text_classifier = TextClassifier(texts, ids)
                self.text_classifier.make_classifier(
                    "topics", ids_filt_topics, filtered_topics)
                self.text_classifier.make_classifier(
                    "subtopics", ids_filt_subtopics, filtered_subtopics)
            except Exception as e:
                print e

    def get_question(self, question_id):
        question = models.Question.query.get(question_id)
        return question

    def search_from_url(self):
        query = self.query_from_url()
        return self.search(query)

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
        """Recives an item of the resut list [(result, best_words)]
            and a dict of filter_ids and decides whether that element is
            accepted by the filter or not.
        """
        result_only = result[0]
        comparators = [True if getattr(result_only, k) == v[0].id else False
                       for k, v in filter_ids.iteritems() if len(v)>0]
        if all(comparators):
            return True
        else:
            return False


    def _filter_results(self, results, filters):
        filt_models = {'tema': ('topic_id', models.Topic),
                       'subtema': ('subtopic_id', models.SubTopic),
                       'autor': ('author_id', models.Author),
                       'informe': ('report_id', models.Report),
                       'organismo-requerido': ('answerer_id', models.Answerer),
                       }
        filt_ids = {v[0]: v[1].query.filter_by(name=filters[k]).all()
                    for k, v in filt_models.iteritems() if k in filters.keys()}
        return filter(lambda x: self._filt_fun(x, filt_ids), results)

    def get_similar_to(self, question_id):
        query = self.query_from_url()
        query['text'] = question_id
        return self.search(query)

    def _search_similar(self, question_id):
        if self.text_classifier is None:
            return []
        ids_sim, dist, best_words = self.text_classifier.get_similar(str(question_id), max_similars=self.per_page)
        ids_sim = map(int, ids_sim)
        results = []
        for qid in ids_sim:
            results.append(models.Question.query.get(qid))
        return zip(results, best_words)

    def suggest_tags(self, tag_type, question_id):
        tags, vals = self.text_classifier.classify(tag_type, [str(question_id)])
        if tag_type == 'topics':
            myModel = models.Topic
        elif tag_type == 'subtopics':
            myModel = models.SubTopic
        else:
            raise(ValueError, "No such model")
        tag_names = [myModel.query.get(idt).name for idt in tags]
        sorted_tags = [x for (y, x) in sorted(zip(vals.tolist()[0], tag_names))]
        return list(reversed(sorted_tags))

    def query_from_url(self):
        filter_titles = ['tema',
                         'subtema',
                         'autor',
                         'informe',
                         'organismo-requerido',
                         'pregunta']
        return {
            'text': request.args.get('q'),
            'current_page': int(request.args.get('pagina', 1)),
            'can_add_more_filters': True,
            'filters': {t: request.args.get(t).lower() for t in filter_titles
                        if request.args.get(t) is not None}
        }

    def url_maker(self, query, page=None):
        args = {}
        if 'text' in query and query['text'] is not None:
            args['q'] = query['text']
        if page is not None:
            args['pagina'] = page
        return url_for('search', **args)
