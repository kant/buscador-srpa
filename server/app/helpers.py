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
            self.text_classifier = TextClassifier(texts, ids)

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
        return self._paginate(results, query)

    def _paginate(self, results, query):
        pagination = {
            'current_page': query['current_page'],
            'total_pages': int(math.ceil(len(results) / float(self.per_page))),
            'total_results': len(results)
        }
        from_position = (pagination['current_page']-1) * self.per_page
        to_position = pagination['current_page'] * self.per_page
        return {
            'pagination': pagination,
            'result_list': results[from_position:to_position],
            'query': query
        }

    def get_similar_to(self, question_id):
        query = self.query_from_url()
        query['text'] = question_id
        return self.search(query)

    def _search_similar(self, question_id):
        ids_sim, dist, best_words = self.text_classifier.get_similar(str(question_id), max_similars=self.per_page)
        ids_sim = map(int, ids_sim)
        results = []
        for qid in ids_sim:
            results.append(models.Question.query.get(qid))
        return zip(results, best_words)

    def _search_by_text(self, text):
        ids_sim, dist, best_words = self.text_classifier.get_similar(text, max_similars=self.per_page)
        ids_sim = map(int, ids_sim)
        results = []
        for qid in ids_sim:
            results.append(models.Question.query.get(qid))
        return results

    def query_from_url(self):
        return {
            'text': request.args.get('q'),
            'current_page': int(request.args.get('pagina', 1)),
            'can_add_more_filters': True,
            'filters': []
        }

    def url_maker(self, query, page=None):
        args = {}
        if 'text' in query and query['text'] is not None:
            args['q'] = query['text']
        if page is not None:
            args['pagina'] = page
        return url_for('search', **args)
