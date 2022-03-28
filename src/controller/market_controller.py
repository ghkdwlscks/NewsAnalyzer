"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk

import requests


class MarketController:
    """MarketController object.
    """

    def __init__(self, **kwargs):
        self.models = {
            "crawler": kwargs["crawler"],
        }
        self.views = {
            "browser": kwargs["browser_view"],
            "button": kwargs["button_view"],
            "market": kwargs["market_view"]
        }

        self.selected_post = None

    def run(self, num_pages, stop_signal):
        """Run MarketWatcher.

        Args:
            num_pages (int): Number of pages to be crawled.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
        """

        self.views["button"].buttons["run"]["text"] = "Running..."
        self.views["button"].buttons["cancel"]["state"] = tk.NORMAL

        self.views["market"].post_listbox.delete(0, tk.END)

        try:
            post_list = self.crawl(num_pages, stop_signal)
            self.views["market"].display_posts(post_list)
        except InterruptedError:
            pass

        self.views["button"].buttons["run"]["state"] = tk.NORMAL
        self.views["button"].buttons["run"]["text"] = "Run"
        self.views["button"].buttons["cancel"]["state"] = tk.DISABLED

    def crawl(self, num_pages, stop_signal):
        """Crawl market posts from the given number of pages.

        Args:
            num_pages (int): Number of pages to be crawled.
            stop_signal (Callable[[], bool]): Function that returns stop signal.

        Returns:
            list[MarketPost]: List of MarketPost objects.
        """

        try:
            post_list = self.models["crawler"].run(num_pages, stop_signal)
        except requests.exceptions.ConnectionError:
            return None

        return post_list

    def post_clicked(self, index):
        """Open market post.

        Args:
            index (int): Index of MarketView.post_listbox.
        """

        self.selected_post = self.views["market"].post_list[index]
        self.views["browser"].open_browser(self.selected_post.url)
