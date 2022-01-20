"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""


import struct
import tkinter as tk

import requests


class MainController:
    """MainController object.

    Kwargs:
        clusterer (clusterer): Clusterer object.
        crawler (Crawler): Crawler object.
        vectorizer (Vectorizer): Vectorizer object.
        article_view (ArticleView): ArticleView object.
        button_view (ButtonView): ButtonView object.
        cluster_view (ClusterView): ClusterView object.
    """

    def __init__(self, **kwargs):
        self.clusterer = kwargs["clusterer"]
        self.crawler = kwargs["crawler"]
        self.vectorizer = kwargs["vectorizer"]
        self.article_view = kwargs["article_view"]
        self.button_view = kwargs["button_view"]
        self.cluster_view = kwargs["cluster_view"]

    def load_fasttext_model(self, fasttext_path):
        """Load pretrained FastText model.

        Args:
            fasttext_path: Pretrained FastText model path.
        """

        for run_label in self.button_view.run_labels:
            run_label.destroy()
        self.button_view.run_labels = []

        try:
            self.vectorizer.load_fasttext_model(fasttext_path)
        except (NotImplementedError, TypeError, struct.error):
            error_message = tk.Label(self.button_view, fg="red", text="Invalid FastText model!")
            error_message.pack(anchor=tk.NW)
            self.button_view.run_labels.append(error_message)
            self.button_view.load_model_button["state"] = tk.NORMAL
            self.button_view.load_model_button["text"] = "Reload model"
            self.button_view.buttons["config"]["state"] = tk.NORMAL
            return

        self.button_view.load_model_button["font"] = ("맑은 고딕", 10)
        self.button_view.load_model_button["text"] = "Model loaded!"
        self.button_view.buttons["run"]["state"] = tk.NORMAL
        self.button_view.buttons["config"]["state"] = tk.DISABLED
        tk.Label(self.button_view, fg="green", text="Model loaded!").pack(anchor=tk.NW)

    def run(self, num_pages, keywords, stop_signal):
        """Run NewsAnalyzer.

        Args:
            num_pages (int): Number of pages to be crawled.
            keywords (list[str]): List of keywords to include and keywords to exclude.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
        """

        self.button_view.buttons["run"]["text"] = "Running..."
        self.button_view.buttons["cancel"]["state"] = tk.NORMAL

        for run_label in self.button_view.run_labels:
            run_label.destroy()
        self.button_view.run_labels = []

        self.article_view.article_details.delete("1.0", tk.END)
        self.article_view.disable_buttons()
        self.cluster_view.cluster_listbox.delete(0, tk.END)

        try:
            article_list = self.crawl(num_pages, keywords, stop_signal)
            if article_list:
                self.vectorize(article_list, stop_signal)
                self.button_view.buttons["cancel"]["state"] = tk.DISABLED
                self.cluster(article_list)
        except InterruptedError:
            stop_message = tk.Label(self.button_view, fg="red", text="Stopped!")
            stop_message.pack(anchor=tk.NW)
            self.button_view.run_labels.append(stop_message)

        self.button_view.buttons["run"]["state"] = tk.NORMAL
        self.button_view.buttons["run"]["text"] = "Run"
        self.button_view.buttons["cancel"]["state"] = tk.DISABLED
        self.button_view.buttons["config"]["state"] = tk.NORMAL

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
        message = tk.Label(self.button_view, textvariable=progress)
        message.pack(anchor=tk.NW)
        self.button_view.run_labels.append(message)

        def update_progress(num_targets, num_processed):
            progress.set(f"Crawling... ({num_processed}/{num_targets})")

        try:
            article_list = self.crawler.run(num_pages, keywords, update_progress, stop_signal)
        except requests.exceptions.ConnectionError:
            error_message = tk.Label(self.button_view, fg="red", text="Disconnected!")
            error_message.pack(anchor=tk.NW)
            self.button_view.run_labels.append(error_message)
            return None

        if stop_signal():
            return None

        message["fg"] = "green"

        return article_list

    def vectorize(self, article_list, stop_signal):
        """Vectorize articles.

        Args:
            article_list (list[Article]): List of Article objects.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
        """

        progress = tk.StringVar(value=f"Vectorizing... (0/{len(article_list)})")
        message = tk.Label(self.button_view, textvariable=progress)
        message.pack(anchor=tk.NW)
        self.button_view.run_labels.append(message)

        num_vectorized = 0
        for article in article_list:
            if stop_signal():
                return
            self.vectorizer.run(article)
            num_vectorized += 1
            progress.set(f"Vectorizing... ({num_vectorized}/{len(article_list)})")

        message["fg"] = "green"

    def cluster(self, article_list):
        """Cluster articles.

        Args:
            article_list (list[Article]): List of Article objects.
        """

        message = tk.Label(self.button_view, text="Clustering...")
        message.pack(anchor=tk.NW)
        self.button_view.run_labels.append(message)

        cluster_list = self.clusterer.run(article_list)

        message["fg"] = "green"
        message["text"] += " Done!"

        self.cluster_view.display_cluster(cluster_list)

    def display_article_details(self, index):
        """Display article details.

        Args:
            index (int): Index of ClusterView.cluster_listbox.
        """

        line_count = 0
        for cluster in self.cluster_view.cluster_list:
            line_count += 1
            if line_count + len(cluster) > index:
                self.article_view.display_article_details(cluster[index - line_count])
                return
            line_count += len(cluster)
