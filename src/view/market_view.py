"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk
import tkinter.font as tkFont


class MarketView(tk.Frame):
    """MarketView object.

    Args:
        parent (MarketWatcher): MarketWatcher object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.market_controller = None

        title = tk.Label(self, font=("맑은 고딕", 15, tkFont.BOLD), text="Market Posts")
        title.pack(anchor=tk.NW)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.post_list = None

        self.post_listbox = tk.Listbox(
            self, font=("맑은 고딕", 10), yscrollcommand=scrollbar.set
        )
        self.post_listbox.pack(anchor=tk.NW, expand=tk.TRUE, fill=tk.BOTH, side=tk.LEFT)

        scrollbar["command"] = self.post_listbox.yview
        self.post_listbox.bind("<<ListboxSelect>>", self.post_clicked)

    def set_controller(self, market_controller):
        """Set controller.

        Args:
            market_controller (MarketController): MarketController object.
        """

        self.market_controller = market_controller

    def display_posts(self, post_list):
        """Dispaly market posts.

        Args:
            post_list (list[MarketPost]): List of MarketPost objects.
        """

        self.post_list = post_list

        for post in self.post_list:
            self.post_listbox.insert(tk.END, post.title)

    def post_clicked(self, event):
        """Open market post.

        Args:
            event (tkinter.Event): Current event.
        """

        if event.widget.size():
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                self.market_controller.post_clicked(index)
