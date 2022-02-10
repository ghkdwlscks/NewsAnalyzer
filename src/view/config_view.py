"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
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
        self.resizable(False, False)
        self.geometry(
            f"+{self.parent.parent.winfo_x() + 210}+{self.parent.parent.winfo_y() + 90}"
        )
        self.focus_set()

        tk.Button(
            self, command=self.save_clicked, text="Save", width=10
        ).pack(anchor=tk.NE, padx=(20, 0), side=tk.RIGHT)

        self.configs = {
            "keywords_to_include": tk.StringVar(value=self.config_controller.keywords_to_include()),
            "keywords_to_exclude": tk.StringVar(value=self.config_controller.keywords_to_exclude()),
            "fasttext_path": tk.StringVar(value=self.config_controller.fasttext_path()),
            "train_enabled": tk.BooleanVar(value=self.config_controller.train_enabled()),
            "trained_model": tk.StringVar(value=self.config_controller.trained_model())
        }

        keyword_frame = tk.Frame(self)
        keyword_frame.pack(anchor=tk.NW)

        tk.Label(
            keyword_frame, font=("맑은 고딕", 10, tkFont.BOLD), text="Keyword Configurations"
        ).pack(anchor=tk.NW)

        tk.Label(keyword_frame, text="Include").pack(anchor=tk.NW, padx=(10, 0))
        tk.Entry(
            keyword_frame, textvariable=self.configs["keywords_to_include"], width=50
        ).pack(anchor=tk.NW, padx=(10, 0))

        tk.Label(keyword_frame, text="Exclude").pack(anchor=tk.NW, padx=(10, 0))
        tk.Entry(
            keyword_frame, textvariable=self.configs["keywords_to_exclude"], width=50
        ).pack(anchor=tk.NW, padx=(10, 0))

        fasttext_frame = tk.Frame(self)
        fasttext_frame.pack(anchor=tk.NW)

        tk.Label(
            fasttext_frame, font=("맑은 고딕", 10, tkFont.BOLD), text="FastText Configurations"
        ).pack(anchor=tk.NW, pady=(50, 0))

        tk.Label(fasttext_frame, text="FastText model path").pack(anchor=tk.NW, padx=(10, 0))
        tk.Entry(
            fasttext_frame,
            readonlybackground="white",
            state="readonly",
            textvariable=self.configs["fasttext_path"],
            width=50
        ).pack(anchor=tk.NW, padx=(10, 0))
        tk.Button(
            fasttext_frame, command=self.browse_clicked, text="Browse"
        ).pack(anchor=tk.E)

        tk.Checkbutton(
            fasttext_frame,
            command=self.check_button_clicked,
            text="Enable training",
            variable=self.configs["train_enabled"]
        ).pack(anchor=tk.NW, padx=(10, 0))

        tk.Label(fasttext_frame, text="Trained model name").pack(anchor=tk.NW, padx=(10, 0))
        self.trained_model_entry = tk.Entry(
            fasttext_frame,
            state=tk.NORMAL if self.configs["train_enabled"].get() else tk.DISABLED,
            textvariable=self.configs["trained_model"],
            width=50
        )
        self.trained_model_entry.pack(anchor=tk.NW, padx=(10, 0))

    def save_clicked(self):
        """Save configurations.
        """

        self.config_controller.save()
        self.destroy()

    def browse_clicked(self):
        """Browse pretrained FastText model path.
        """

        fasttext_path = tkFileDialog.askopenfilename(
            initialdir=f"{os.getcwd()}/fasttext", parent=self
        )

        if fasttext_path:
            self.configs["fasttext_path"].set(fasttext_path)

    def check_button_clicked(self):
        """Switch the state of trained model entry.
        """

        if self.configs["train_enabled"].get():
            self.trained_model_entry["state"] = tk.NORMAL
        else:
            self.trained_model_entry["state"] = tk.DISABLED
