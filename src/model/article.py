"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


from dataclasses import dataclass

import numpy as np


@dataclass
class Article:
    """Article object.

    Args:
        title (str): Title.
        press (str): Press.
        time (str): Time.
        origin_url (str): Origin URL.
        naver_url (str): NAVER URL.
        document (list[list[str]]): Document split by sentences, then words.
        article_vector (numpy.ndarray, optional): Vectorized article. Defaults to np.zeros(300).
    """

    title: str
    press: str
    time: str
    origin_url: str
    naver_url: str
    document: list[list[str]]
    article_vector: np.ndarray = np.zeros(300)
