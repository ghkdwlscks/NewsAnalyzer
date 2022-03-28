"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk

from controller.market_controller import MarketController
from model.market_crawler import MarketCrawler
from view.browser_view import BrowserView
from view.market_button_view import MarketButtonView
from view.market_view import MarketView


class MarketWatcher(tk.Frame):
    """MarketWatcher object.

    Args:
        parent (Main): Main object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # Models
        market_crawler = MarketCrawler()

        # Views
        browser_view = BrowserView(self)
        browser_view.pack(fill=tk.BOTH, padx=10, pady=10, side=tk.RIGHT)
        button_view = MarketButtonView(self)
        button_view.pack(fill=tk.BOTH, padx=10, pady=10, side=tk.RIGHT)
        market_view = MarketView(self)
        market_view.pack(expand=tk.TRUE, fill=tk.BOTH, padx=10, pady=10)

        # Controllers
        market_controller = MarketController(
            crawler=market_crawler,
            browser_view=browser_view,
            button_view=button_view,
            market_view=market_view
        )
        button_view.set_controller(market_controller)
        market_view.set_controller(market_controller)
