"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import hdbscan
import numpy as np


class Clusterer:
    """Clusterer object.

    Args:
        min_cluster_size (int, optional): Minimum number of articles to form a cluster.
                                          Larger min_cluster_size generates larger cluster.
                                          Defaults to 2.
        min_samples (int, optional): Minimum number of neighbors to be a core point.
                                     Larger min_samples generates more noises.
                                     Defaults to 2.
    """

    def __init__(self, min_cluster_size=2, min_samples=2):
        self.min_cluster_size = min_cluster_size
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

        clusters = self.cluster(article_vectors)

        num_clusters = max(clusters) + 2
        cluster_list = [[] for _ in range(num_clusters)]

        for i, _ in enumerate(article_vectors):
            cluster_list[clusters[i]].append(article_list[i])

        return cluster_list

    def cluster(self, article_vectors):
        """Cluster articles.

        Args:
            article_vectors (numpy.ndarray): Numpy array of article vectors.

        Returns:
            numpy.ndarray: Numpy array of labels.
        """

        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            prediction_data=True
        ).fit(article_vectors)

        return clusterer.labels_
