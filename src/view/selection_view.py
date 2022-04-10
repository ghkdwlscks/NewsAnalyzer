"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk
import tkinter.font as tkFont


class SelectionView(tk.Frame):
    """SelectionView object.

    Args:
        parent (NewsAnalyzer): NewsAnalyzer object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.news_controller = None

        title = tk.Label(self, font=("맑은 고딕", 15, tkFont.BOLD), text="Selected Articles")
        title.pack(anchor=tk.NW)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.selection_list = []

        self.selection_listbox = tk.Listbox(
            self, font=("맑은 고딕", 10), takefocus=tk.FALSE, yscrollcommand=scrollbar.set
        )
        self.selection_listbox.pack(anchor=tk.NW, expand=tk.TRUE, fill=tk.BOTH, side=tk.LEFT)

        scrollbar["command"] = self.selection_listbox.yview
        self.selection_listbox.bind("<<ListboxSelect>>", self.article_clicked)

    def set_controller(self, news_controller):
        """Set controller.

        Args:
            news_controller (NewsController): NewsController object.
        """

        self.news_controller = news_controller

    def article_clicked(self, _):
        """Activate delete button.
        """

        self.news_controller.enable_selection_buttons(True)

    def add_to_list(self, article):
        """Add selected article to listbox.

        Args:
            article (Article): Article object.
        """

        self.selection_list.append(article)
        self.selection_listbox.insert(tk.END, article.title)

    def delete_from_list(self):
        """Delete selected article from listbox.
        """

        self.selection_list.pop(self.selection_listbox.curselection()[0])
        self.selection_listbox.delete(self.selection_listbox.curselection())

        self.news_controller.enable_selection_buttons(False)
