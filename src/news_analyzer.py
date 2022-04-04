"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk

from controller.config_controller import ConfigController
from controller.news_controller import NewsController
from model.clusterer import Clusterer
from model.config import Config
from model.news_crawler import NewsCrawler
from model.vectorizer import Vectorizer
from view.browser_view import BrowserView
from view.news_button_view import NewsButtonView
from view.cluster_view import ClusterView


class NewsAnalyzer(tk.Frame):
    """NewsAnalyzer object.

    Args:
        parent (Main): Main object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # Models
        config = Config()
        clusterer = Clusterer()
        crawler = NewsCrawler()
        vectorizer = Vectorizer()

        # Views
        browser_view = BrowserView(self)
        browser_view.pack(fill=tk.BOTH, padx=10, pady=10, side=tk.RIGHT)
        button_view = NewsButtonView(self)
        button_view.pack(fill=tk.BOTH, padx=10, pady=10, side=tk.RIGHT)
        cluster_view = ClusterView(self)
        cluster_view.pack(expand=tk.TRUE, fill=tk.BOTH, padx=10, pady=10)

        # Controllers
        config_controller = ConfigController(config)
        news_controller = NewsController(
            clusterer=clusterer,
            crawler=crawler,
            vectorizer=vectorizer,
            browser_view=browser_view,
            button_view=button_view,
            cluster_view=cluster_view,
            config_controller=config_controller
        )
        button_view.set_controllers(news_controller, config_controller)
        cluster_view.set_controller(news_controller)
