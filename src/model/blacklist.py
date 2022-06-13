"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


from datetime import datetime

import pandas as pd


class Blacklist():
    """Blacklist object.
    """

    def __init__(self):
        self.dataframe = None

        try:
            self.dataframe = pd.read_csv("data/blacklist.csv", index_col=False)
        except FileNotFoundError:
            self.dataframe = pd.DataFrame(columns=["추가 날짜", "닉네임", "이메일", "휴대폰"])


    def add(self, market_post):
        """Add market post to the file.

        Args:
            market_post (MarketPost): MarketPost object.
        """

        new_data = pd.DataFrame([[
            datetime.today().strftime("%y/%m/%d"),
            market_post.nickname,
            market_post.email,
            market_post.phone if market_post.phone != "null" else ""
        ]], columns=["추가 날짜", "닉네임", "이메일", "휴대폰"])
        self.dataframe = pd.concat([self.dataframe, new_data], ignore_index=True)

    def save(self):
        """Save as csv file.
        """

        self.dataframe.to_csv("data/blacklist.csv", index=False)
