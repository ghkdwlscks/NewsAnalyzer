"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import tkinter as tk
import tkinter.font as tkFont

from cefpython3 import cefpython as cef


class BrowserView(tk.Frame):
    """BrowserView object.

    Args:
        parent (tk.Frame): tkinter.Frame object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.news_controller = None

        title = tk.Label(self, font=("맑은 고딕", 15, tkFont.BOLD), text="Browser")
        title.pack(anchor=tk.NW)

        self.browser_frame = tk.Frame(self, width=1080)
        self.browser_frame.pack(expand=tk.TRUE, fill=tk.BOTH)

        self.browser = None

    def set_controller(self, news_controller):
        """Set controller.

        Args:
            news_controller (NewsController): NewsController object.
        """

        self.news_controller = news_controller

    def open_browser(self, url):
        """Open article.

        Args:
            url (str): URL of the article.
        """

        if not self.browser:
            window_info = cef.WindowInfo()
            window_info.SetAsChild(
                self.browser_frame.winfo_id(),
                [0, 0, self.browser_frame.winfo_width(), self.browser_frame.winfo_height()]
            )
            self.browser = cef.CreateBrowserSync(window_info, url=url)
            self.loop()
        else:
            self.browser.LoadUrl(url)

    def loop(self):
        """Loop CEF Python.
        """

        cef.MessageLoopWork()
        self.after(10, self.loop)
