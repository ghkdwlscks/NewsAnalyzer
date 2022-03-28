"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import re
from datetime import datetime
from functools import partial
from multiprocessing import Value
from multiprocessing.pool import ThreadPool

import psutil
import requests
from bs4 import BeautifulSoup

from model.article import Article


class NewsCrawler:
    """NewsCrawler object.
    """

    def __init__(self):
        self.url_prefix = "https://search.naver.com/search.naver?where=news&query="
        self.url_postfix = "&nso=so%3Add%2Cp%3Aall"
        self.keyword_fix = None

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

        self.keyword_fix = keywords[0].replace(",", "+%7C+")
        if keywords[1]:
            self.keyword_fix += "+-"
            self.keyword_fix += keywords[1].replace(",", "+-")

        search_url_list = [self.get_page_url(index) for index in range(num_pages)]

        with ThreadPool(psutil.cpu_count()) as pool:
            num_targets = Value("i", 0)
            get_article_list = partial(
                self.get_article_list, num_targets, update_progress, stop_signal
            )
            target_articles = pool.map(get_article_list, search_url_list)
        target_articles = [article for page in target_articles for article in page]
        target_articles = self.eliminate_duplicates(target_articles)
        target_articles.reverse()

        with ThreadPool(psutil.cpu_count(logical=False)) as pool:
            num_processed = Value("i", 0)
            process_article = partial(
                self.process_article,
                num_processed,
                partial(update_progress, len(target_articles)),
                stop_signal
            )
            article_list = pool.map(process_article, target_articles)

        return article_list

    def get_page_url(self, page_index):
        """Get page URL of the index.

        Args:
            page_index (int): Page index.

        Returns:
            str: Page URL of the index.
        """

        page_postfix = "&start=" + str(page_index * 10 + 1)

        return self.url_prefix + self.keyword_fix + self.url_postfix + page_postfix

    @classmethod
    def get_article_list(cls, num_targets, update_progress, stop_signal, search_url):
        """Get article tag list from the given URL.

        Args:
            num_targets (multiprocessing.Value): Number of targets.
            update_progress (Callable[[int, int], None]): Function that updates crawling progress.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
            search_url (str): Page URL to get articles from.

        Returns:
            list[bs4.element.Tag]: List of article tags.
        """

        raw = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        html = BeautifulSoup(raw.text, "lxml")

        article_list = [
            article for article in html.select("ul.list_news > li") if cls.get_urls(article)[1]
        ]

        if stop_signal():
            raise InterruptedError

        with num_targets.get_lock():
            num_targets.value += len(article_list)
            update_progress(num_targets.value, 0)

        return article_list

    @classmethod
    def eliminate_duplicates(cls, target_articles):
        """Eliminate duplicate articles.

        Args:
            target_articles (list[bs4.element.Tag]): List of article tags.

        Returns:
            list[bs4.element.Tag]: List of unique article tags.
        """

        unique_articles = []
        duplicate_checker = set()

        for article in target_articles:
            naver_url = cls.get_urls(article)[1]
            if naver_url not in duplicate_checker:
                unique_articles.append(article)
                duplicate_checker.add(naver_url)

        return unique_articles

    @classmethod
    def process_article(cls, num_processed, update_progress, stop_signal, article):
        """Process article tag to Article object.

        Args:
            num_processed (multiprocessing.Value): Number of processed articles.
            update_progress (Callable[[int], None]): Function that updates crawling progress.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
            article (bs4.element.Tag): Tag of the article.

        Returns:
            Article: Article object.
        """

        title = cls.get_title(article)
        press = cls.get_press(article)
        origin_url, naver_url = cls.get_urls(article)
        document = cls.get_document(naver_url)

        if stop_signal():
            raise InterruptedError

        with num_processed.get_lock():
            num_processed.value += 1
            update_progress(num_processed.value)

        return Article(title, press, origin_url, naver_url, document)

    @classmethod
    def get_title(cls, article):
        """Get title of the given article tag.

        Args:
            article (bs4.element.Tag): Tag of the article.

        Returns:
            str: Title of the article.
        """

        return article.select_one("a.news_tit")["title"]

    @classmethod
    def get_press(cls, article):
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

    @classmethod
    def get_urls(cls, article):
        """Get URL of the given article tag.

        Args:
            article (bs4.element.Tag): Tag of the article.

        Returns:
            tuple[str, str]: Origin and NAVER URLs of the article.
        """

        origin_url = article.select_one("a.news_tit")["href"]
        if len(article.select("a.info")) == 2:
            naver_url = article.select("a.info")[1]["href"]
        else:
            naver_url = None

        return origin_url, naver_url

    @classmethod
    def get_document(cls, naver_url):
        """Get document of article from the given URL.

        Args:
            naver_url (str): NAVER URL of the article.

        Returns:
            list[list[str]]: Document split by sentences, then words.
        """

        raw = requests.get(naver_url, headers={"User-Agent": "Mozilla/5.0"})
        html = BeautifulSoup(raw.text, "lxml")
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
            file_name = "error_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"
            with open(file_name, "w", encoding="utf-8") as error_log:
                error_log.write("Error URL: " + naver_url)

        return [sentence.split() for sentence in sentences]
