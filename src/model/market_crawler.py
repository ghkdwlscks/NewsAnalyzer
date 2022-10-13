"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import re

import requests
from bs4 import BeautifulSoup

from model.market_post import MarketPost


class MarketCrawler:
    """MarketCrawler object.
    """

    url_prefix = (
        "https://search.naver.com/search.naver?sm=tab_hty.top&where=articlec&query="
    )
    url_postfix = "&st=date"

    def run(self, num_pages, stop_signal):
        """Crawl posts from the given number of pages.

        Args:
            num_pages (int): Number of pages to be crawled.
            stop_signal (Callable[[], bool]): Function that returns stop signal.

        Returns:
            list[MarketPost]: List of MarketPost objects.
        """

        post_list = []

        keywords = ["군복", "군수품", "군용", "군용마스크", "방독면", "실탄", "육군", "전투화", "탄피"]
        keyword_fix = "+%7C+".join(keywords)

        search_url_list = [self.get_page_url(keyword_fix, index) for index in range(num_pages)]
        post_url_list = []

        for search_url in search_url_list:
            post_url_list += self.get_post_url_list(search_url)
            if stop_signal():
                raise InterruptedError

        for post_url in post_url_list:
            post = self.get_post(post_url)
            if post:
                post_list.append(post)
            if stop_signal():
                raise InterruptedError

        return post_list

    @classmethod
    def get_page_url(cls, keyword_fix, page_index):
        """Get page URL of the index.

        Args:
            keyword_fix (str): Keyword query.
            page_index (int): Page index.

        Returns:
            str: Page URL of the index.
        """

        page_postfix = f"&start={str(page_index * 10 + 1)}"

        return cls.url_prefix + keyword_fix + cls.url_postfix + page_postfix

    @classmethod
    def get_post_url_list(cls, search_url):
        """Get post tag list from the given URL.

        Args:
            search_url (str): Page URL to get posts from.

        Returns:
            list[bs4.element.Tag]: List of post tags.
        """

        raw = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        html = BeautifulSoup(raw.text, "lxml")

        post_url_list = [article.attrs["href"] for article in html.select("div.total_area > a")]

        return post_url_list

    @classmethod
    def get_post(cls, post_url):
        """Get details of the given post url.

        Args:
            post_url (str): URL of the post.

        Returns:
            MarketPost: MarketPost object.
        """

        re_compiled = {
            "error": re.compile(r"errorCode"),
            "clubid": re.compile(r"(?<=clubid=)[0-9]+"),
            "articleid": re.compile(r"(?<=ArticleRead\.nhn\?articleid=)[0-9]+"),
            "title": re.compile(r"(?<=\"subject\":\").*?(?=\",\")"),
            "nickname": re.compile(r"(?<=\"nick\":\").*?(?=\")"),
            "phone": re.compile(r"(?<=\"phoneNo\":\")[0-9-]+"),
            "email": re.compile(r"(?<=\"email\":\").+?(?=\")")
        }

        raw = requests.get(post_url, headers={"User-Agent": "Mozilla/5.0"})

        clubid = re.search(re_compiled["clubid"], raw.text).group()
        articleid = re.search(re_compiled["articleid"], raw.text).group()

        document_url = (
            "https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/"
            f"{clubid}/articles/{articleid}"
        )

        raw = requests.get(document_url, headers={"User-Agent": "Mozilla/5.0"})
        raw_text = re.sub(r"\\n", " ", raw.text)
        raw_text = re.sub(r"\\(?=\")", "", raw_text)
        html = BeautifulSoup(raw_text, "lxml")

        if re.search(re_compiled["error"], raw_text):
            return None

        title = re.search(re_compiled["title"], raw_text).group()
        nickname = re.search(re_compiled["nickname"], raw_text).group()
        try:
            email = re.search(re_compiled["email"], raw_text).group()
        except AttributeError:
            email = "null"
        try:
            phone = re.search(re_compiled["phone"], raw_text).group()
        except AttributeError:
            phone = "null"
        document = "\n".join([line.text for line in html.select("p.se-text-paragraph")])

        return MarketPost(post_url, title, nickname, email, phone, document)
