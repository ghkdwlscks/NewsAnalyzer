"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk

import requests

from model.blacklist import Blacklist


class MarketController:
    """MarketController object.
    """

    def __init__(self, **kwargs):
        self.models = {
            "crawler": kwargs["crawler"],
        }
        self.views = {
            "blacklist": kwargs["blacklist_view"],
            "browser": kwargs["browser_view"],
            "button": kwargs["button_view"],
            "market": kwargs["market_view"]
        }

        self.selected_post = None

        self.blacklist = Blacklist()

    def run(self, num_pages, stop_signal):
        """Run MarketWatcher.

        Args:
            num_pages (int): Number of pages to be crawled.
            stop_signal (Callable[[], bool]): Function that returns stop signal.
        """

        self.views["button"].buttons["run"]["text"] = "실행 중..."
        self.views["button"].buttons["cancel"]["state"] = tk.NORMAL
        self.views["button"].buttons["add_to_blacklist"]["state"] = tk.DISABLED

        for run_label in self.views["button"].run_labels:
            run_label.destroy()

        self.views["button"].run_labels = []
        self.views["blacklist"].blacklist_listbox.delete(0, tk.END)
        self.views["market"].post_listbox.delete(0, tk.END)

        try:
            post_list, blacklist = self.crawl(num_pages, stop_signal)
            if post_list:
                self.views["market"].display_posts(post_list)
            if blacklist:
                self.views["blacklist"].display_blacklist(blacklist)
        except InterruptedError:
            pass

        self.views["button"].buttons["run"]["state"] = tk.NORMAL
        self.views["button"].buttons["run"]["text"] = "실행"
        self.views["button"].buttons["cancel"]["state"] = tk.DISABLED

    def crawl(self, num_pages, stop_signal):
        """Crawl market posts from the given number of pages.

        Args:
            num_pages (int): Number of pages to be crawled.
            stop_signal (Callable[[], bool]): Function that returns stop signal.

        Returns:
            tuple[list[MarketPost], list[MarketPost]]: List of MarketPost objects and blacklist.
        """

        try:
            post_list = self.models["crawler"].run(num_pages, stop_signal)
        except requests.exceptions.ConnectionError:
            error_message = tk.Label(self.views["button"], fg="red", text="Disconnected!")
            error_message.pack(anchor=tk.NW)
            self.views["button"].run_labels.append(error_message)
            return None, None

        blacklist = []
        blacklist_emails = self.blacklist.dataframe["이메일"].values
        for post in post_list:
            if post.email in blacklist_emails:
                blacklist.append(post)

        return post_list, blacklist

    def post_clicked(self, index, blacklist=False):
        """Open market post.

        Args:
            index (int): Index of MarketView.post_listbox.
        """

        if not blacklist:
            self.selected_post = self.views["market"].post_list[index]
            self.views["button"].buttons["add_to_blacklist"]["state"] = tk.NORMAL
        else:
            self.selected_post = self.views["blacklist"].blacklist[index]
            self.views["button"].buttons["add_to_blacklist"]["state"] = tk.DISABLED
        self.views["browser"].open_browser(self.selected_post.url)

    def add_to_blacklist(self, market_post=None):
        """Add to blacklist.

        Args:
            market_post (MarketPost, optional): MarketPost object. Defaults to None.
        """

        if market_post:
            self.blacklist.add(market_post)
        else:
            self.blacklist.add(self.selected_post)

        self.blacklist.save()
