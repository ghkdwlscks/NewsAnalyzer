"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from cefpython3 import cefpython as cef

from market_watcher import MarketWatcher
from news_analyzer import NewsAnalyzer


class Main(tk.Tk):
    """Main object.
    """

    def __init__(self):
        super().__init__()

        self.title("News Analyzer")
        self.attributes("-fullscreen", tk.TRUE)
        self.resizable(tk.FALSE, tk.FALSE)

        tkFont.nametofont("TkDefaultFont").configure(family="맑은 고딕", size=10)

        style = ttk.Style()
        style.configure("Tab", font=("맑은 고딕", 11), padding=3)
        style.layout(
            "Tab",
            [("Notebook.tab", {"sticky": tk.NSEW, "children": [
                ("Notebook.padding", {"side": tk.TOP, "sticky": tk.NSEW, "children": [
                    ("Notebook.label", {"side": tk.TOP, "sticky": ""})
                ]})
            ]})]
        )

        tk.Label(
            self, font=("Calibri", 10), text="Jinchan Hwang, jchwang@yonsei.ac.kr"
        ).pack(anchor=tk.SE, side=tk.BOTTOM)

        notebook = ttk.Notebook(self, padding=5)
        notebook.pack(fill=tk.BOTH, expand=tk.TRUE)

        news_analyzer = NewsAnalyzer(self)
        notebook.add(news_analyzer, text="NewsAnalyzer")

        market_watcher = MarketWatcher(self)
        notebook.add(market_watcher, text="MarketWatcher")

        notebook.enable_traversal()

        notebook.bind("<<NotebookTabChanged>>", lambda event: event.widget.focus())


if __name__ == "__main__":
    os.chdir(f"{os.path.expanduser('~')}/Desktop/NewsAnalyzer")
    main = Main()
    cef.Initialize()
    main.mainloop()
    cef.Shutdown()
