"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import re
import struct
from pickle import UnpicklingError

import numpy as np
from gensim import models


class Vectorizer:
    """Vectorizer object.

    Args:
        weight (float, optional): Weight of title in article vector. Defaults to 0.2.
    """

    def __init__(self, weight=0.2):
        self.weight = weight
        self.model = None


    def load_fasttext_model(self, fasttext_model_path):
        """Load pretrained FastText model.

        Args:
            fasttext_model_path (str): Pretrained FastText model path.
        """

        try:
            self.model = models.fasttext.FastTextKeyedVectors.load(fasttext_model_path)
        except UnpicklingError:
            try:
                self.model = models.fasttext.load_facebook_model(fasttext_model_path)
            except (NotImplementedError, TypeError, struct.error) as invalid_model_error:
                raise RuntimeError from invalid_model_error

    def update_fasttext_model(self, sentences, model_name):
        """Update and save FastText model.

        Args:
            sentences (list[list[str]]): List of sentences, which is list of words.
            model_name (str): Name of trained model to be saved.
        """

        self.model.build_vocab(sentences, update=True)
        self.model.train(
            sentences, total_examples=self.model.corpus_count, epochs=self.model.epochs
        )
        self.model.save(f"fasttext/{model_name}")

    def run(self, article):
        """Vectorize the given article.

        Args:
            article (Article): Article object.
        """

        title = article.title
        title = re.sub(r"[^0-9A-Za-z가-힣]", " ", title)
        title = re.sub(r"\s+", " ", title)
        title = title.split()

        title_vector = np.zeros(300)
        for word in title:
            word_vector = self.model.wv.get_vector(word, norm=True)
            title_vector += word_vector
        if title_vector.any():
            title_vector /= np.linalg.norm(title_vector)

        document_vector = np.zeros(300)
        for sentence in article.document:
            sentence_vector = np.zeros(300)
            for word in sentence:
                word_vector = self.model.wv.get_vector(word, norm=True)
                sentence_vector += word_vector
            if sentence_vector.any():
                sentence_vector /= np.linalg.norm(sentence_vector)
            document_vector += sentence_vector
        if document_vector.any():
            document_vector /= np.linalg.norm(document_vector)

        article_vector = title_vector * self.weight + document_vector * (1 - self.weight)
        if article_vector.any():
            article_vector /= np.linalg.norm(article_vector)

        article.article_vector = article_vector
