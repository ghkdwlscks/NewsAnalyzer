"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


from dataclasses import dataclass


@dataclass
class MarketPost:
    """MarketPost object.

    Args:
        title (str): Title.
        url (str): URL.
        document (str): Document.
        phone (str): Phone number.
        email (str): Email address.
    """

    title: str
    url: str
    document: str
    phone: str
    email: str
