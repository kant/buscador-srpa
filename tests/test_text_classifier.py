"""Tests del modulo text_classifier."""
import unittest
import sys
import os
import codecs
import numpy as np
sys.path.insert(0, os.path.abspath('..'))
from text_classifier import TextClassifier


class TestTextClassifier(unittest.TestCase):

    """Clase de tests del objeto TextClassifier."""

    def setUp(self):
        """Carga de los datos de prueba (20 Newsgroups corpus)."""
        TEST_DIR = "/home/mec/testData/textos/20_newsgroups/"
        cats = os.listdir(TEST_DIR)
        cats_totales = []
        contenidos = []
        for cat in cats:
            temp_list = os.listdir(os.path.join(TEST_DIR, cat))
            cats_totales = cats_totales + [cat] * len(temp_list)
            temp_list = map(lambda x: os.path.join(TEST_DIR, cat, x),
                            temp_list)
            for filename in temp_list:
                with codecs.open(
                        filename, encoding='latin1', mode='r') as content_file:
                    lines = content_file.readlines()
                    content = ''.join(lines[11:])
                contenidos.append(content)
        # sacar los textos muy cortos
        contenidos = filter(lambda x: len(x) > 100, contenidos)
        self.ids = [x[0] for x in contenidos]
        self.texts = contenidos
        self.labels = cats_totales
        self.tc = TextClassifier(self.texts, self.ids)

    def test_reload_texts(self):
        # TODO aca van los tests!
        self.assertEqual(12, 12)

    def test_classifier_performance(self):
        cantidad_datos = len(self.ids)
        mitad_datos = cantidad_datos / 2
        self.tc.make_classifier("prueba",
                                self.ids[:mitad_datos],
                                self.labels[:mitad_datos])
        clasificador = getattr(self.tc, "prueba")
        otra_mitad = self.ids[mitad_datos:]
        X_test = self.tc.tfidf_mat[mitad_datos:, :]
        y_test = self.labels[mitad_datos:]
        my_score = clasificador.score(X_test, y_test)
        self.assertEqual('aaa', 'aaa')

if __name__ == '__main__':
    unittest.main()
