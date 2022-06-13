"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


from dataclasses import dataclass


@dataclass
class MarketPost:
    """MarketPost object.

    Args:
        url (str): URL.
        title (str): Title.
        nickname (str): Nickname.
        email (str): Email address.
        phone (str): Phone number.
        document (str): Document.
    """

    url: str
    title: str
    nickname: str
    email: str
    phone: str
    document: str
