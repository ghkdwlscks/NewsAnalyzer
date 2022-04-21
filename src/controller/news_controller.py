"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk
from datetime import datetime

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
            "selection": kwargs["selection_view"]
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
        self.views["button"].buttons["add"]["state"] = tk.DISABLED
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
        self.views["button"].buttons["add"]["state"] = tk.DISABLED
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
                    self.views["button"].buttons["add"]["state"] = tk.DISABLED
                    return
                self.selected_article = cluster[index - line_count]
                self.views["button"].buttons["pdf"]["state"] = tk.NORMAL
                if self.selected_article not in self.views["selection"].selection_list:
                    self.views["button"].buttons["add"]["state"] = tk.NORMAL
                else:
                    self.views["button"].buttons["add"]["state"] = tk.DISABLED
                self.views["browser"].open_browser(self.selected_article.naver_url)
                return
            line_count += len(cluster)

    def add_to_list(self):
        """Add selected article to selection list.
        """

        self.views["selection"].add_to_list(self.selected_article)

        self.views["button"].buttons["add"]["state"] = tk.DISABLED

    def save_pdf(self):
        """Save PDF.
        """

        self.views["browser"].browser.Print()

    def export_text_format(self):
        """Export text format.
        """

        text_format_path = "format/text_" + datetime.now().strftime("%Y%m%d") + ".txt"

        day = datetime.now().weekday()
        if not day:
            day = "월"
        elif day == 1:
            day = "화"
        elif day == 2:
            day = "수"
        elif day == 3:
            day = "목"
        elif day == 4:
            day = "금"
        elif day == 5:
            day = "토"
        else:
            day = "일"

        num_articles = len(self.views["selection"].selection_list)

        number_list = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]

        with open(text_format_path, "w", encoding="utf-8") as text_format_file:
            header = (
                "[사이버순찰 '" + datetime.now().strftime("%y. %m. %d.") +
                f" ({day})]\n\n\n[ 기타 ] : {num_articles}건\n\n"
            )
            text_format_file.write(header)
            for i, article in enumerate(self.views["selection"].selection_list):
                text_format_file.write(
                    f"{number_list[i]}. {article.title} [{article.press} {article.time[-5:]}]\n\n"
                    f"기사 URL: {article.origin_url}\n\n"
                )
            text_format_file.write("\n육군수사단 과학수사센터\n사이버범죄수사대")

    def delete_from_list(self):
        """Delete selected article from selection list.
        """

        self.views["selection"].delete_from_list()

    def enable_selection_buttons(self, enable):
        """Activate selection buttons.

        Args:
            enable (bool): Whether to enable delete button.
        """

        if enable:
            self.views["button"].buttons["text"]["state"] = tk.NORMAL
            self.views["button"].buttons["report"]["state"] = tk.NORMAL
            self.views["button"].buttons["delete"]["state"] = tk.NORMAL
        else :
            self.views["button"].buttons["text"]["state"] = tk.DISABLED
            self.views["button"].buttons["report"]["state"] = tk.DISABLED
            self.views["button"].buttons["delete"]["state"] = tk.DISABLED
