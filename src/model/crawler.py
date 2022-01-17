"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""



import re

import requests
from bs4 import BeautifulSoup

from model.article import Article


class Crawler:
    """Crawler object.
    """

    def __init__(self):
        self.url_prefix = "https://search.naver.com/search.naver?where=news&query="
        self.url_postfix = "&nso=so%3Add%2Cp%3Aall"

    def run(self, num_pages, keywords, update_progress, stop_signal):
        """Crawl articles from the given number of pages.

        Args:
            num_pages (int): Number of pages to be crawled.
            keywords (list[str]): List of keywords to include and keywords to exclude.
            update_progress (Callable[[int, int], None]): Function that updates crawling progress.
            stop_signal (Callable[[], bool]): Function that returns stop signal.

        Returns:
            list[Article]: List of Article objects.
        """

        keyword_fix = keywords[0].replace(",", "+%7C+")
        if keywords[1]:
            keyword_fix += "+-"
            keyword_fix += keywords[1].replace(",", "+-")

        target_articles = []
        duplicate_checker = set()
        for index in range(num_pages):
            if stop_signal():
                return None
            search_url = (
                self.url_prefix + keyword_fix + self.url_postfix + self.get_page_postfix(index)
            )
            articles = self.get_article_list(search_url)
            for article in articles:
                naver_url = self.get_urls(article)[1]
                if naver_url and naver_url not in duplicate_checker:
                    target_articles.append((article, naver_url))
                    duplicate_checker.add(naver_url)
                    update_progress(len(target_articles), 0)
        target_articles.reverse()

        article_list = []
        for article in target_articles:
            if stop_signal():
                return None
            article_list.append(
                Article(
                    self.get_title(article[0]),
                    self.get_press(article[0]),
                    *self.get_urls(article[0]),
                    self.get_document(article[1])
                )
            )
            update_progress(len(target_articles), len(article_list))

        return article_list

    @staticmethod
    def get_page_postfix(page_index):
        """Get URL postfix of the page index.

        Args:
            page_index (int): Page index.

        Returns:
            str: URL postfix of the page index.
        """

        return "&start=" + str(page_index * 10 + 1)

    @staticmethod
    def get_article_list(search_url):
        """Get article tag list from the given URL.

        Args:
            search_url (str): URL to get articles from.

        Returns:
            bs4.element.ResultSet: List of article tags.
        """

        raw = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")

        return html.select("ul.list_news > li")

    @staticmethod
    def get_title(article):
        """Get title of the given article tag.

        Args:
            article (bs4.element.Tag): Tag of the article.

        Returns:
            str: Title of the article.
        """

        return article.select_one("a.news_tit")["title"]

    @staticmethod
    def get_press(article):
        """Get press of the given article tag.

        Args:
            article (bs4.element.Tag): Tag of the article.

        Returns:
            str: Press of the article.
        """

        press = article.select_one("a.info.press").text
        if article.select_one("i.spnew.ico_pick"):
            press = press[:-6]

        return press

    @staticmethod
    def get_urls(article):
        """Get URL of the given article tag.

        Args:
            article (bs4.element.Tag): Tag of the article.

        Returns:
            tuple[str, str]: Original and NAVER URLs of the article.
        """

        origin_url = article.select_one("a.news_tit")["href"]
        if len(article.select("a.info")) == 2:
            naver_url = article.select("a.info")[1]["href"]
        else:
            naver_url = None

        return origin_url, naver_url

    @staticmethod
    def get_document(url):
        """Get document of article from the given URL.

        Args:
            url (str): NAVER URL of the article.

        Returns:
            list[list[str]]: Document split by sentences, then words.
        """

        raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")
        if html.select_one("div._article_body_contents.article_body_contents"):
            document = html.select_one("div._article_body_contents.article_body_contents").text
        elif html.select_one("div.article_body"):
            document = html.select_one("div.article_body").text
        elif html.select_one("div.news_end"):
            document = html.select_one("div.news_end").text

        try:
            document = document.replace("\n", " ").replace("\t", " ").replace(
                "// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", " "
            )
            document = re.sub(r"[0-9A-Za-z_.+-]+@[0-9A-Za-z-.]+\.[0-9A-Za-z-.]+", " ", document)
            document = re.sub(r"[^0-9A-Za-z가-힣. ]", " ", document)
            document = re.sub(r"\s+", " ", document)
            document = re.sub(r"^\s", "", document)
            document = re.sub(r"\.{2,}", ".", document)
            document = re.sub(r"(?<=[가-힣])\.\s*", ".\n", document)
            document = re.sub(r"\n.*[^.]\n", "\n", document)
            document = re.sub(r"\n+", "\n", document)
            document = re.sub(r"\.", "", document)
            document = re.sub(r"[\n ]$", "", document)

            sentences = document.splitlines()

        except UnboundLocalError:
            document = [[]]
            print("Error URL: " + url)

        return [sentence.split() for sentence in sentences]
