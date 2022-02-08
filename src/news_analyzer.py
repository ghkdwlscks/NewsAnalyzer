"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import os
import tkinter as tk
import tkinter.font as tkFont

from controller.config_controller import ConfigController
from controller.main_controller import MainController
from model.clusterer import Clusterer
from model.config import Config
from model.crawler import Crawler
from model.vectorizer import Vectorizer
from view.article_view import ArticleView
from view.button_view import ButtonView
from view.cluster_view import ClusterView


class NewsAnalyzer(tk.Tk):
    """News Analyzer object.
    """

    def __init__(self):
        super().__init__()

        self.title("News Analyzer")
        self.resizable(False, False)
        self.geometry("+500+200")

        tkFont.nametofont("TkDefaultFont").configure(family="맑은 고딕", size=10)

        tk.Label(
            self, font=("Calibri", 9), text="Jinchan Hwang, jchwang@yonsei.ac.kr"
        ).pack(anchor=tk.SE, side=tk.BOTTOM)

        # Models
        config = Config()
        clusterer = Clusterer()
        crawler = Crawler()
        vectorizer = Vectorizer()

        # Views
        article_view = ArticleView(self)
        article_view.pack(expand=True, fill=tk.BOTH, padx=10, pady=10, side=tk.BOTTOM)
        button_view = ButtonView(self)
        button_view.pack(expand=True, fill=tk.BOTH, padx=10, pady=10, side=tk.RIGHT)
        cluster_view = ClusterView(self)
        cluster_view.pack(expand=True, fill=tk.BOTH, padx=10, pady=10, side=tk.LEFT)

        # Controllers
        config_controller = ConfigController(config)
        main_controller = MainController(
            clusterer=clusterer, crawler=crawler, vectorizer=vectorizer,
            article_view=article_view, button_view=button_view, cluster_view=cluster_view,
            config_controller=config_controller
        )
        article_view.set_controller(main_controller)
        button_view.set_controllers(main_controller, config_controller)
        cluster_view.set_controller(main_controller)


if __name__ == "__main__":
    os.chdir("C:/Users/User/Desktop/NewsAnalyzer")
    news_analyzer = NewsAnalyzer()
    news_analyzer.mainloop()
