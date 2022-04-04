"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk

import requests


class NewsController:
    """NewsController object.
    """

    def __init__(self, **kwargs):
        self.models = {
            "clusterer": kwargs["clusterer"],
            "crawler": kwargs["crawler"],
            "vectorizer": kwargs["vectorizer"]
        }
        self.views = {
            "browser": kwargs["browser_view"],
            "button": kwargs["button_view"],
            "cluster": kwargs["cluster_view"],
        }
        self.controllers = {"config": kwargs["config_controller"]}

        self.lastest_fasttext_model = None

        self.selected_article = None

    def load_fasttext_model(self):
        """Load pretrained FastText model.
        """

        for run_label in self.views["button"].run_labels:
            run_label.destroy()

        self.views["button"].run_labels = []
        self.views["button"].buttons["url"]["state"] = tk.DISABLED
        self.views["button"].buttons["naver_url"]["state"] = tk.DISABLED
        self.views["cluster"].cluster_listbox.delete(0, tk.END)

        try:
            self.models["vectorizer"].load_fasttext_model(
                self.controllers["config"].fasttext_path()
            )
        except RuntimeError:
            error_message = tk.Label(self.views["button"], fg="red", text="Invalid FastText model!")
            error_message.pack(anchor=tk.NW)
            self.views["button"].run_labels.append(error_message)
            self.views["button"].buttons["load"]["state"] = tk.NORMAL
            self.views["button"].buttons["load"]["text"] = "Reload model"
            self.views["button"].buttons["config"]["state"] = tk.NORMAL
            return

        self.lastest_fasttext_model = self.controllers["config"].fasttext_path()

        self.views["button"].buttons["load"]["font"] = ("맑은 고딕", 10)
        self.views["button"].buttons["load"]["text"] = "Model loaded!"
        self.views["button"].buttons["run"]["state"] = tk.NORMAL
        self.views["button"].buttons["config"]["state"] = tk.NORMAL

    def run(self, num_pages, stop_signal):
        """Run NewsAnalyzer.

        Args:
            num_pages (int): Number of pages to be crawled.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
        """

        self.views["button"].buttons["run"]["text"] = "Running..."
        self.views["button"].buttons["cancel"]["state"] = tk.NORMAL

        for run_label in self.views["button"].run_labels:
            run_label.destroy()

        self.views["button"].run_labels = []
        self.views["button"].buttons["url"]["state"] = tk.DISABLED
        self.views["button"].buttons["naver_url"]["state"] = tk.DISABLED
        self.views["cluster"].cluster_listbox.delete(0, tk.END)

        try:
            keywords = [
                self.controllers["config"].keywords_to_include(),
                self.controllers["config"].keywords_to_exclude()
            ]
            article_list = self.crawl(num_pages, keywords, stop_signal)
            if stop_signal():
                raise InterruptedError
            if article_list:
                if self.controllers["config"].train_enabled():
                    self.train(article_list)
                if stop_signal():
                    raise InterruptedError
                self.vectorize(article_list, stop_signal)
                self.views["button"].buttons["cancel"]["state"] = tk.DISABLED
                self.cluster(article_list)
        except InterruptedError:
            stop_message = tk.Label(self.views["button"], fg="red", text="Stopped!")
            stop_message.pack(anchor=tk.NW)
            self.views["button"].run_labels.append(stop_message)

        self.views["button"].buttons["run"]["state"] = tk.NORMAL
        self.views["button"].buttons["run"]["text"] = "Run"
        self.views["button"].buttons["cancel"]["state"] = tk.DISABLED
        self.views["button"].buttons["config"]["state"] = tk.NORMAL

    def crawl(self, num_pages, keywords, stop_signal):
        """Crawl articles from the given number of pages.

        Args:
            num_pages (int): Number of pages to be crawled.
            keywords (list[str]): List of keywords to include and keywords to exclude.
            stop_signal (Callable[[], bool]): Function that returns stop signal.

        Returns:
            list[Article]: List of Article objects.
        """

        progress = tk.StringVar(value="Crawling... (0/0)")
        message = tk.Label(self.views["button"], textvariable=progress)
        message.pack(anchor=tk.NW)
        self.views["button"].run_labels.append(message)

        def update_progress(num_targets, num_processed):
            progress.set(f"Crawling... ({num_processed}/{num_targets})")

        try:
            article_list = self.models["crawler"].run(
                num_pages,
                keywords,
                update_progress,
                stop_signal
            )
        except requests.exceptions.ConnectionError:
            error_message = tk.Label(self.views["button"], fg="red", text="Disconnected!")
            error_message.pack(anchor=tk.NW)
            self.views["button"].run_labels.append(error_message)
            return None

        if stop_signal():
            raise InterruptedError

        message["fg"] = "green"

        return article_list

    def train(self, article_list):
        """Update and save FastText model.

        Args:
            article_list (list[Article]): List of Article objects.
        """

        message = tk.Label(self.views["button"], text="Training...")
        message.pack(anchor=tk.NW)
        self.views["button"].run_labels.append(message)

        sentences = []
        for article in article_list:
            sentences += article.document
        self.models["vectorizer"].update_fasttext_model(
            sentences,
            self.controllers["config"].trained_model()
        )

        message["fg"] = "green"
        message["text"] += " Done!"

    def vectorize(self, article_list, stop_signal):
        """Vectorize articles.

        Args:
            article_list (list[Article]): List of Article objects.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
        """

        progress = tk.StringVar(value=f"Vectorizing... (0/{len(article_list)})")
        message = tk.Label(self.views["button"], textvariable=progress)
        message.pack(anchor=tk.NW)
        self.views["button"].run_labels.append(message)

        num_vectorized = 0
        for article in article_list:
            if stop_signal():
                raise InterruptedError
            self.models["vectorizer"].run(article)
            num_vectorized += 1
            progress.set(f"Vectorizing... ({num_vectorized}/{len(article_list)})")

        message["fg"] = "green"

    def cluster(self, article_list):
        """Cluster articles.

        Args:
            article_list (list[Article]): List of Article objects.
        """

        message = tk.Label(self.views["button"], text="Clustering...")
        message.pack(anchor=tk.NW)
        self.views["button"].run_labels.append(message)

        cluster_list = self.models["clusterer"].run(article_list)

        message["fg"] = "green"
        message["text"] += " Done!"

        self.views["cluster"].display_clusters(cluster_list)

    def article_clicked(self, index):
        """Open article.

        Args:
            index (int): Index of ClusterView.cluster_listbox.
        """

        line_count = -1
        for cluster in self.views["cluster"].cluster_list:
            line_count += 2
            if line_count + len(cluster) > index:
                if index - line_count < 0:
                    self.views["button"].buttons["url"]["state"] = tk.DISABLED
                    self.views["button"].buttons["naver_url"]["state"] = tk.DISABLED
                    return
                self.selected_article = cluster[index - line_count]
                self.views["button"].buttons["pdf"]["state"] = tk.NORMAL
                self.views["button"].buttons["url"]["state"] = tk.NORMAL
                self.views["button"].buttons["naver_url"]["state"] = tk.NORMAL
                self.views["browser"].open_browser(self.selected_article.naver_url)
                return
            line_count += len(cluster)

    def save_pdf(self):
        """Save PDF.
        """

        self.views["browser"].browser.Print()
