# -*- coding: utf-8 -*-
u"""Módulo de clasificación de textos.

Este módulo contiene a los objetos que permiten entrenar un clasificador
automático de textos.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py
Todo:
    * For module TODOs
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


class TextClassifier():

    u"""Clasificador automático de textos.

    Usa TF-IDF para vectorizar.
    Usa SVM para clasificar.
    Usa Ball-Tree para devolver vecinos cercanos.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__():
        """Definido en la declaracion de la clase."""
        pass

    def __str__():
        """Representacion en str del objeto."""
        pass

    def train():
        """Entrenar un clasificador SVM sobre los textos cargados.

        Nota:
            Usa el clasificador de `Scikit-learn <http://scikit-learn.org/>`_
        """
        pass

    def retrain():
        """Reentrenar incrementalmente un clasificador SVM sobre los textos
        cargados.

        Nota:
            Usa el clasificador de `Scikit-learn <http://scikit-learn.org/>`_
        """
        pass

    def classify(self, examples, max_labels=1, goodness_of_fit=False):
        """Usar un clasificador SVM para etiquetar textos nuevos.

        Nota:
            Usa el clasificador de `Scikit-learn <http://scikit-learn.org/>`_

        Args:
            examples (list or str): Se espera un ejemplo o una lista de
                ejemplos a clasificar en texto plano.
            max_labels (int, optional): Cantidad de etiquetas a devolver para
                cada ejemplo. Si se devuelve mas de una el orden corresponde a
                la plausibilidad de cada etiqueta.
            goodness_of_fit (bool, optional): Indica si devuelve o no una
                medida de cuan buenas son las etiquetas.
        """
        pass

    def get_similar(self, example, max_similars=3, similarity_cutoff=None):
        """Devuelve textos similares al ejemplo dentro de los textos entrenados.

        Nota:
            Usa la distancia de coseno del vector de features TF-IDF

        Args:
            example (str): Se espera un texto a partir del cual se buscaran
                otros textos similares.
            max_similars (int, optional): Cantidad de textos similares a
                devolver.
            similarity_cutoff (float, optional): Valor umbral de similaridad
                para definir que dos textos son similares entre si.
        """
        pass

    def search(self, query):
        u"""2DO: Aún no esta claro que sea distinta de get_similar."""
        pass

    def save_model():
        """Guarda el modelo (tanto el SVM como Ball-Tree) a disco."""
        pass

    def load_model():
        """Carga el modelo (tanto el SVM como Ball-Tree) del disco."""
        pass
