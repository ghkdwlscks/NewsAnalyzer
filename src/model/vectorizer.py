"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import re

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

        self.model = models.fasttext.load_facebook_model(fasttext_model_path)

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
