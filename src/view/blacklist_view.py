"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk
import tkinter.font as tkFont


class BlacklistView(tk.Frame):
    """BlacklistView object.

    Args:
        parent (MarketWatcher): MarketWatcher object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.market_controller = None

        title = tk.Label(self, font=("맑은 고딕", 15, tkFont.BOLD), text="Blacklist")
        title.pack(anchor=tk.NW)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.blacklist = []

        self.blacklist_listbox = tk.Listbox(
            self, font=("맑은 고딕", 10), takefocus=tk.FALSE, yscrollcommand=scrollbar.set
        )
        self.blacklist_listbox.pack(anchor=tk.NW, expand=tk.TRUE, fill=tk.BOTH, side=tk.LEFT)

        scrollbar["command"] = self.blacklist_listbox.yview
        self.blacklist_listbox.bind("<<ListboxSelect>>", self.blacklist_clicked)

    def set_controller(self, market_controller):
        """Set controller.

        Args:
            market_controller (MarketController): MarketController object.
        """

        self.market_controller = market_controller

    def display_blacklist(self, blacklist):
        """Dispaly blacklist.
        """

        self.blacklist = blacklist

        for post in self.blacklist:
            self.blacklist_listbox.insert(tk.END, post.title)

    def blacklist_clicked(self, event):
        """Open blacklist post.

        Args:
            event (tkinter.Event): Current event.
        """

        if event.widget.size():
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                self.market_controller.post_clicked(index, True)
