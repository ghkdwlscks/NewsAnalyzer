"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import numpy as np
from hdbscan import HDBSCAN


class Clusterer:
    """Clusterer object.

    Args:
        min_samples (int, optional): Minimum number of articles to form a cluster. Defaults to 2.
    """

    def __init__(self, min_samples=2):
        self.min_samples = min_samples

    def run(self, article_list):
        """Cluster articles.

        Args:
            article_list (list[Article]): List of Article objects.

        Returns:
            list[list[Article]]: Clustered Article objects.
        """

        article_vectors = []
        for article in article_list:
            article_vectors.append(article.article_vector)
        article_vectors = np.array(article_vectors)

        clusters = HDBSCAN(
            min_samples=self.min_samples,
            cluster_selection_method="leaf"
        ).fit_predict(article_vectors)

        num_clusters = max(clusters) + 2
        cluster_list = [[] for _ in range(num_clusters)]

        for i, _ in enumerate(article_vectors):
            cluster_list[clusters[i]].append(article_list[i])

        return cluster_list
