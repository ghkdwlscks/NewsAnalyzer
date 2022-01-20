"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""


from dataclasses import dataclass

import numpy as np


@dataclass
class Article:
    """Article object.

    Args:
        title (str): Title.
        press (str): Press.
        origin_url (str): Origin URL.
        naver_url (str): NAVER URL.
        document (list[list[str]]): Document split by sentences, then words.
        article_vector (numpy.ndarray, optional): Vectorized article. Defaults to np.zeros(300).
    """

    title: str
    press: str
    origin_url: str
    naver_url: str
    document: list[list[str]]
    article_vector: np.ndarray = np.zeros(300)

    def __eq__(self, other):
        """Return whether two objects are equivalent.

        Args:
            other (Article): Article object.

        Returns:
            bool: True if two Article object are equivalent, False otherwise.
        """

        return self.naver_url == other.naver_url

    def __hash__(self):
        """Hash function.

        Returns:
            str: NAVER URL.
        """

        return hash(self.naver_url)
