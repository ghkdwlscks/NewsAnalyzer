"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import re
import tkinter as tk
import tkinter.font as tkFont


class ClusterView(tk.Frame):
    """ClusterView object.

    Args:
        parent (NewsAnalyzer): NewsAnalyzer object.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.main_controller = None

        title = tk.Label(self, font=("맑은 고딕", 13, tkFont.BOLD), text="Clustered Articles")
        title.pack(anchor=tk.NW)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cluster_list = None

        self.cluster_listbox = tk.Listbox(
            self, font=("맑은 고딕", 10), height=20, width=100, yscrollcommand=scrollbar.set
        )
        self.cluster_listbox.pack(anchor=tk.NW, expand=True, fill=tk.X, side=tk.LEFT)

        scrollbar["command"] = self.cluster_listbox.yview
        self.cluster_listbox.bind("<<ListboxSelect>>", self.article_clicked)

    def set_controller(self, main_controller):
        """Set controller

        Args:
            main_controller (MainController): MainController object.
        """

        self.main_controller = main_controller

    def display_cluster(self, cluster_list):
        """Dispaly clustered articles.

        Args:
            cluster_list (list[list[Article]]): Clustered article objects.
        """

        self.cluster_list = cluster_list

        font = tkFont.Font(font=("맑은 고딕", 10))

        article_list = [article for cluster in cluster_list for article in cluster]
        max_press_width = max(
            [font.measure(article.press, self.cluster_listbox) for article in article_list]
        )
        space_width = font.measure(" ", self.cluster_listbox)

        for i, cluster in enumerate(self.cluster_list):
            if i != len(self.cluster_list) - 1:
                cluster_number = f"Cluster {i} ({len(cluster)})"
            else:
                cluster_number = "Noise"
            if i:
                self.cluster_listbox.insert(tk.END, "")
            self.cluster_listbox.insert(tk.END, cluster_number)
            for article in cluster:
                press_width = font.measure(article.press, self.cluster_listbox)
                padding = (max_press_width - press_width) // space_width + 2
                self.cluster_listbox.insert(tk.END, article.press + " " * padding + article.title)

    def article_clicked(self, event):
        """Display article details.

        Args:
            event (tkinter.Event): Current event.
        """

        if event.widget.size():
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                title = event.widget.get(index)
                if title and not re.match(r"Cluster.*", title):
                    self.main_controller.display_article_details(index)
                else:
                    self.main_controller.clear_article_details()
