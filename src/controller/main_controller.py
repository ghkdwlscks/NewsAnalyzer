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
            self.button_view.config_button["state"] = tk.NORMAL
            return

        self.button_view.load_model_button["font"] = ("맑은 고딕", 10)
        self.button_view.load_model_button["text"] = "Model loaded!"
        self.button_view.run_button["state"] = tk.NORMAL
        self.button_view.config_button["state"] = tk.DISABLED
        tk.Label(self.button_view, fg="green", text="Model loaded!").pack(anchor=tk.NW)

    def run(self, num_pages, keywords_to_include, keywords_to_exclude):
        """Run NewsAnalyzer.

        Args:
            num_pages (int): Number of pages to be crawled.
            keywords_to_include (str): Keywords to include.
            keywords_to_exclude (str): Keywords to exclude.
        """

        for run_label in self.button_view.run_labels:
            run_label.destroy()
        self.button_view.run_labels = []

        self.article_view.article_details.delete("1.0", tk.END)
        self.article_view.disable_buttons()
        self.cluster_view.cluster_listbox.delete(0, tk.END)

        article_list = self.crawl(num_pages, keywords_to_include, keywords_to_exclude)
        if article_list:
            self.vectorize(article_list)
            self.cluster(article_list)

        self.button_view.run_button["state"] = tk.NORMAL
        self.button_view.config_button["state"] = tk.NORMAL

    def crawl(self, num_pages, keywords_to_include, keywords_to_exclude):
        """Crawl articles from the given number of pages.

        Args:
            num_pages (int): Number of pages to be crawled.
            keywords_to_include (str): Keywords to include.
            keywords_to_exclude (str): Keywords to exclude.

        Returns:
            list[Article]: List of Article objects.
        """

        progress = tk.StringVar(value="Crawling... (0/0)")
        message = tk.Label(self.button_view, textvariable=progress)
        message.pack(anchor=tk.NW)
        self.button_view.run_labels.append(message)

        def update_progress(num_targets, num_crawled):
            progress.set(f"Crawling... ({num_crawled}/{num_targets})")

        try:
            article_list = self.crawler.run(
                num_pages, keywords_to_include, keywords_to_exclude, update_progress
            )
        except requests.exceptions.ConnectionError:
            error_message = tk.Label(self.button_view, fg="red", text="Disconnected!")
            error_message.pack(anchor=tk.NW)
            self.button_view.run_labels.append(error_message)
            return None

        message["fg"] = "green"

        return article_list

    def vectorize(self, article_list):
        """Vectorize articles.

        Args:
            article_list (list[Article]): List of Article objects.
        """

        progress = tk.StringVar(value=f"Vectorizing... (0/{len(article_list)})")
        message = tk.Label(self.button_view, textvariable=progress)
        message.pack(anchor=tk.NW)
        self.button_view.run_labels.append(message)

        num_vectorized = 0
        for article in article_list:
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
