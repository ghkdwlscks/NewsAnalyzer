"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""


import tkinter as tk
import tkinter.font as tkFont
import webbrowser as wb


class ArticleView(tk.Frame):
    """ArticleView object.

    Args:
        parent (NewsAnalyzer): NewsAnalyzer object.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.main_controller = None

        title = tk.Label(self, font=("맑은 고딕", 13, tkFont.BOLD), text="Article Details")
        title.pack(anchor=tk.NW)

        self.article_details = tk.Text(self, font=("맑은 고딕", 10), height=6)
        self.article_details.pack(expand=True, fill=tk.X)

        self.selected_article = None

        link_frame = tk.Frame(self)
        link_frame.pack(anchor=tk.NW, pady=(5, 0))

        self.article_link_button = tk.Button(
            link_frame,
            command=lambda: wb.open(self.selected_article.naver_url),
            state=tk.DISABLED,
            text="Article link",
            width=10
        )
        self.article_link_button.pack(anchor=tk.NW, side=tk.LEFT)

        self.copy_url_button = tk.Button(
            link_frame,
            command=lambda: self.update_clipboard(self.selected_article.origin_url),
            state=tk.DISABLED,
            text="Copy URL",
            width=10
        )
        self.copy_url_button.pack(anchor=tk.NW, padx=(20, 5), side=tk.LEFT)

        self.copy_naver_url_button = tk.Button(
            link_frame,
            command=lambda: self.update_clipboard(self.selected_article.naver_url),
            state=tk.DISABLED,
            text="Copy NAVER URL",
            width=16
        )
        self.copy_naver_url_button.pack(anchor=tk.NW, side=tk.LEFT)

    def set_controller(self, main_controller):
        """Set controller.

        Args:
            main_controller (MainController): MainController object.
        """

        self.main_controller = main_controller

    def display_article_details(self, article):
        """Display article details.

        Args:
            article (Article): Article object.
        """

        self.selected_article = article
        self.enable_buttons()

        self.article_details.delete("1.0", tk.END)
        self.article_details.insert(tk.END, "Title: " + article.title)
        self.article_details.insert(tk.END, "\nPress: " + article.press)
        self.article_details.insert(tk.END, "\nURL: " + article.origin_url)
        self.article_details.insert(tk.END, "\nNAVER URL: " + article.naver_url)

    def update_clipboard(self, url):
        """Update clipboard.

        Args:
            url (str): URL of the article.
        """

        self.parent.clipboard_clear()
        self.parent.clipboard_append(url)

    def enable_buttons(self):
        """Enable article link and URL copy buttons.
        """

        self.article_link_button["state"] = tk.NORMAL
        self.copy_url_button["state"] = tk.NORMAL
        self.copy_naver_url_button["state"] = tk.NORMAL

    def disable_buttons(self):
        """Disable article link and URL copy buttons.
        """

        self.article_link_button["state"] = tk.DISABLED
        self.copy_url_button["state"] = tk.DISABLED
        self.copy_naver_url_button["state"] = tk.DISABLED
