"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""


import os
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog


class ConfigView(tk.Toplevel):
    """ConfigView object.

    Args:
        config_controller (ConfigController): ConfigController object.
        parent (ButtonView): ButtonView object.
    """

    def __init__(self, config_controller, parent):
        super().__init__(parent, padx=10, pady=10)

        self.parent = parent

        self.config_controller = config_controller

        self.title("Configurations")
        self.geometry(
            f"+{self.parent.parent.winfo_x() + 400}+{self.parent.parent.winfo_y() + 90}"
        )
        self.focus_set()

        tk.Button(
            self, command=self.save_clicked, text="Save", width=10
        ).pack(anchor=tk.NE, padx=(20, 0), side=tk.RIGHT)

        self.keyword_frame = tk.Frame(self)
        self.keyword_frame.pack(anchor=tk.NW)
        tk.Label(
            self.keyword_frame, font=("맑은 고딕", 10, tkFont.BOLD), text="Keyword Configurations"
        ).pack(anchor=tk.NW)
        tk.Label(self.keyword_frame, text="Include").pack(anchor=tk.NW, padx=(10, 0))
        self.keywords_to_include = tk.StringVar(value=self.config_controller.keywords_to_include())
        tk.Entry(
            self.keyword_frame, textvariable=self.keywords_to_include, width=50
        ).pack(anchor=tk.NW, padx=(10, 0))
        tk.Label(self.keyword_frame, text="Exclude").pack(anchor=tk.NW, padx=(10, 0))
        self.keywords_to_exclude = tk.StringVar(value=self.config_controller.keywords_to_exclude())
        tk.Entry(
            self.keyword_frame, textvariable=self.keywords_to_exclude, width=50
        ).pack(anchor=tk.NW, padx=(10, 0))

        self.fasttext_frame = tk.Frame(self)
        self.fasttext_frame.pack(anchor=tk.NW)
        tk.Label(
            self.fasttext_frame, font=("맑은 고딕", 10, tkFont.BOLD), text="FastText Configurations"
        ).pack(anchor=tk.NW)
        tk.Label(self.fasttext_frame, text="FastText model path").pack(anchor=tk.NW, padx=(10, 0))
        self.fasttext_path = tk.StringVar(value=self.config_controller.fasttext_path())
        tk.Entry(
            self.fasttext_frame,
            readonlybackground="white",
            state="readonly",
            textvariable=self.fasttext_path,
            width=50
        ).pack(anchor=tk.NW, padx=(10, 0))
        tk.Button(
            self.fasttext_frame,
            command=self.browse_clicked,
            text="Browse"
        ).pack(anchor=tk.E)

    def save_clicked(self):
        """Save configurations.
        """

        self.config_controller.save()
        self.destroy()

    def browse_clicked(self):
        """Browse FastText model path.
        """

        self.fasttext_path.set(
            tkFileDialog.askopenfilename(
                initialdir=f"{os.getcwd()}/fasttext", parent=self.fasttext_frame
            )
        )
        self.config_controller.update("FASTTEXT", "PATH", self.fasttext_path.get())
