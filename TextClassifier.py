# -*- coding: utf-8 -*-
u"""Módulo de clasificación de textos.

Este módulo contiene a los objetos que permiten entrenar un clasificador
automático de textos y pedir sugerencias de textos similares.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py
Todo:
    * For module TODOs
"""
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.linear_model import SGDClassifier
from scipy import sparse
import pandas as pd
import numpy as np


class TextClassifier():

    u"""Clasificador automático de textos.

    Usa TF-IDF para vectorizar.
    Usa SVM para clasificar.
    Usa Ball-Tree para devolver vecinos cercanos.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, texts, ids, vocabulary=None):
        """Definido en la declaracion de la clase."""
        es_stopwords = pd.read_csv('ES_stopwords.txt',
                                   header=None, encoding='utf-8')
        es_stopwords = list(np.squeeze(es_stopwords.values))
        self.vectorizer = CountVectorizer(input='content', ngram_range=(1, 1),
                                          min_df=1, stop_words=es_stopwords,
                                          vocabulary=vocabulary)
        self.transformer = TfidfTransformer()
        self.reload_texts(texts, ids)

    def __str__():
        """Representacion en str del objeto."""
        pass

    def make_classifier(self, name, ids, labels):
        """Entrenar un clasificador SVM sobre los textos cargados.

        Args:
            name (str): Nombre para el clasidicador.
            ids (list): Se espera una lista de N ids de textos ya almacenados
                en el TextClassifier.
            labels (list): Se espera una lista de N etiquetas. Una por cada id
                de texto presente en ids.
        Nota:
            Usa el clasificador de `Scikit-learn <http://scikit-learn.org/>`_
        """
        if not all(np.in1d(ids, self.ids)):
            raise ValueError("Hay ids de textos que no se encuentran \
                              almacenados.")
        setattr(self, name, SGDClassifier())
        classifier = getattr(self, name)
        indices = np.in1d(self.ids, ids)
        classifier.fit(self.tfidf_mat[indices, :], labels)

    def retrain(self, name, ids, labels):
        """Reentrenar parcialmente un clasificador SVM.

        Args:
            name (str): Nombre para el clasidicador.
            ids (list): Se espera una lista de N ids de textos ya almacenados
                en el TextClassifier.
            labels (list): Se espera una lista de N etiquetas. Una por cada id
                de texto presente en ids.
        Nota:
            Usa el clasificador de `Scikit-learn <http://scikit-learn.org/>`_
        """
        if not all(np.in1d(ids, self.ids)):
            raise ValueError("Hay ids de textos que no se encuentran \
                              almacenados.")
        try:
            classifier = getattr(self, name)
        except AttributeError:
            raise AttributeError("No hay ningun clasificador con ese nombre.")
        indices = np.in1d(self.ids, ids)
        classifier.partial_fit(self.tfidf_mat[indices, :], labels)

    def classify(self, classifier_name, examples, max_labels=1,
                 goodness_of_fit=False):
        """Usar un clasificador SVM para etiquetar textos nuevos.

        Nota:
            Usa el clasificador de `Scikit-learn <http://scikit-learn.org/>`_

        Args:
            classifier_name (str): Nombre del clasidicador a usar.
            examples (list or str): Se espera un ejemplo o una lista de
                ejemplos a clasificar en texto plano o en ids.
            max_labels (int, optional): Cantidad de etiquetas a devolver para
                cada ejemplo. Si se devuelve mas de una el orden corresponde a
                la plausibilidad de cada etiqueta.
            goodness_of_fit (bool, optional): Indica si devuelve o no una
                medida de cuan buenas son las etiquetas.
        """
        classifier = getattr(self, classifier_name)
        texts_vectors = self._make_text_vectors(examples)
        return classifier.classes_, classifier.decision_function(texts_vectors)

    def _make_text_vectors(self, examples):
        """Funcion para generar los vectores tf-idf de una lista de textos.

        Args:
            examples (list or str): Se espera un ejemplo o una lista de:
                o bien ids, o bien textos.
        """
        if type(examples) is str:
            if examples in self.ids:
                textvec = self.tfidf_mat[self.ids == examples, :]
            else:
                textvec = self.vectorizer.transform([examples])
                textvec = self.transformer.transform(textvec)
                return textvec
        elif type(examples) is list:
            if all(np.in1d(examples, self.ids)):
                return self.tfidf_mat[np.in1d(self.ids, examples)]
            elif not any(np.in1d(examples, self.ids)):
                textvec = self.vectorizer.transform(examples)
                textvec = self.transformer.transform(textvec)
                return textvec
            else:
                raise ValueError("Las listas de ejemplos deben ser todos ids\
                                  de textos almacenados o todos textos planos")
        else:
            raise TypeError("Los ejemplos no son del tipo de dato adecuado.")

    def get_similar(self, example, max_similars=3, similarity_cutoff=None):
        """Devuelve textos similares al ejemplo dentro de los textos entrenados.

        Nota:
            Usa la distancia de coseno del vector de features TF-IDF

        Args:
            example (str): Se espera un id de texto  o un texto a partir del
                cual se buscaran otros textos similares.
            max_similars (int, optional): Cantidad de textos similares a
                devolver.
            similarity_cutoff (float, optional): Valor umbral de similaridad
                para definir que dos textos son similares entre si.
        """
        if max_similars > self.term_mat.shape[0]:
            raise ValueError("No se pueden pedir mas sugerencias que la \
                              cantidad de textos que hay almacenados.")
        if example in self.ids:
            index = self.ids == example
            y = self.tfidf_mat[index, :]
            distances = np.squeeze(pairwise_distances(self.tfidf_mat, y))
            # Pongo la distancia a si mismo como inf, par que no se devuelva a
            # si mismo como una opcion
            distances[index] = np.inf
        else:
            y = self.vectorizer.transform([example])  # contar terminos
            y = self.transformer.transform(y)  # calcular tfidf
            distances = np.squeeze(pairwise_distances(self.tfidf_mat, y))
        I = np.argsort(distances)
        closest_n = I[:max_similars]
        sorted_dist = distances[closest_n]
        if similarity_cutoff:
            closest_n = closest_n[sorted_dist < similarity_cutoff]
        text_ids = self.ids[closest_n]
        return text_ids, sorted_dist

    def reload_texts(self, texts, ids, vocabulary=None):
        """Calcula los vectores de terminos de textos y los almacena.

        A diferencia de :func:`~TextClassifier.TextClassifier.store_text` esta
        funcion borra cualquier informacion almacenada y comienza el conteo
        desde cero. Se usa para redefinir el vocabulario sobre el que se
        construyen los vectores.

        Args:
            texts (list): Una lista de N textos a incorporar.
            ids (list): Una lista de N ids alfanumericos para los textos.
        """
        self.ids = np.array(ids)
        if vocabulary:
            self.vectorizer.vocabulary = vocabulary
        self.term_mat = self.vectorizer.fit_transform(texts)
        self._update_tfidf()

    def store_text(self, texts, ids, replace_texts=False):
        """Calcula los vectores de terminos de un texto y los almacena.

        Nota:
            Esta funcion usa el vocabulario que ya esta almacenado, es decir,
            que no se incorporan nuevos terminos. Si se quiere cambiar el
            vocabulario deben recargarse todos los textos con
            :func:`~TextClassifier.TextClassifier.reload_texts`
        Args:
            texts (list): Una lista de N textos a incorporar.
            ids (list): Una lista de N ids alfanumericos para los textos.
            etiquetas (list, optional): Si esta presente se interpreta que los
                textos deben ser ademas usados para entrenar al clasificador.
            replace_texts (bool, optional): Indica si deben reemplazarse los
                textos cuyo id ya este almacenado. Si es False y algun id ya se
                encuentra almacenado se considera un error.
        """
        if not replace_texts and any(np.in1d(ids, self.ids)):
            raise ValueError("Alguno de los ids provistos ya esta en el \
                              indice")
        else:
            ids = np.array(ids)
            partial_mat = self.vectorizer.transform(texts)
            # Si no hay ids ya guardados solo concateno y los agrego al
            # array self.ids
            if not any(np.in1d(ids, self.ids)):
                self.ids = np.r_[self.ids, ids]
                self.term_mat = sparse.vstack((self.term_mat,
                                               partial_mat))
            # Si los hay,
            else:
                oldrows = np.in1d(self.ids, ids)
                oldpartial = np.in1d(ids, self.ids)
                # Actualizo las filas que ya estaban
                self.term_mat[oldrows, :] = partial_mat[oldpartial, :]
                # y agrego las que no
                partial_mat = partial_mat[~oldpartial, :]
                self.term_mat = sparse.vstack((self.term_mat,
                                               partial_mat))
                self.ids = np.r_[self.ids, ids[~oldpartial]]
        self._update_tfidf()

    def _update_tfidf(self):
        self.tfidf_mat = self.transformer.fit_transform(self.term_mat)
