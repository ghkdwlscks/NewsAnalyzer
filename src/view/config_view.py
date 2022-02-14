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
            f"+{self.parent.parent.winfo_x() + 175}+{self.parent.parent.winfo_y() + 90}"
        )
        self.focus_set()

        tk.Button(
            self, command=self.save_clicked, text="Save", width=10
        ).pack(anchor=tk.NE, padx=(20, 0), pady=20, side=tk.RIGHT)

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
        ).pack(anchor=tk.NW, pady=(5, 5))

        tk.Label(keyword_frame, text="Include").pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))
        tk.Entry(
            keyword_frame, textvariable=self.configs["keywords_to_include"], width=55
        ).pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))

        tk.Label(keyword_frame, text="Exclude").pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))
        tk.Entry(
            keyword_frame, textvariable=self.configs["keywords_to_exclude"], width=55
        ).pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))

        fasttext_frame = tk.Frame(self)
        fasttext_frame.pack(anchor=tk.NW)

        tk.Label(
            fasttext_frame, font=("맑은 고딕", 10, tkFont.BOLD), text="FastText Configurations"
        ).pack(anchor=tk.NW, pady=(50, 5))

        tk.Label(
            fasttext_frame, text="FastText model path"
        ).pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))
        browse_frame = tk.Frame(fasttext_frame)
        browse_frame.pack(anchor=tk.NW, fill=tk.BOTH)
        tk.Entry(
            browse_frame,
            readonlybackground="white",
            state="readonly",
            textvariable=self.configs["fasttext_path"],
            width=50
        ).pack(anchor=tk.NW, padx=(10, 5), pady=(0, 5), side=tk.LEFT)
        tk.Button(
            browse_frame,
            command=self.browse_clicked,
            font=("맑은 고딕", 6, tkFont.BOLD),
            padx=0,
            pady=0,
            text=". . .",
            width=3
        ).pack(anchor=tk.NE, pady=(0, 5), side=tk.RIGHT)

        tk.Checkbutton(
            fasttext_frame,
            command=self.check_button_clicked,
            text="Enable training",
            variable=self.configs["train_enabled"]
        ).pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))

        tk.Label(
            fasttext_frame, text="Trained model name"
        ).pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))
        self.trained_model_entry = tk.Entry(
            fasttext_frame,
            state=tk.NORMAL if self.configs["train_enabled"].get() else tk.DISABLED,
            textvariable=self.configs["trained_model"],
            width=55
        )
        self.trained_model_entry.pack(anchor=tk.NW, padx=(10, 0), pady=(0, 5))

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
