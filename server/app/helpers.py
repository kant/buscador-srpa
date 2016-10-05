#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import models
from flask import request


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
        pass

    @classmethod
    def search(cls):
        results = models.Question.query.all()
        return results

    @classmethod
    def query_from_url(cls):
        return {
            'text': request.args.get('q'),
            'can_add_more_filters': True,
            'filters': []
        }
