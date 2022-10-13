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
        parent (NewsAnalyzer): NewsAnalyzer object.
    """

    def __init__(self, config_controller, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.config_controller = config_controller

        self.title("Configurations")
        self.resizable(False, False)

        tk.Button(
            self, command=self.save_clicked, text="Save", width=10
        ).pack(anchor=tk.NE, padx=(10, 0), pady=(10, 0), side=tk.RIGHT)

        self.configs = {
            "keywords_to_include": tk.StringVar(value=self.config_controller.keywords_to_include()),
            "keywords_to_exclude": tk.StringVar(value=self.config_controller.keywords_to_exclude()),
            "fasttext_path": tk.StringVar(value=self.config_controller.fasttext_path()),
            "train_enabled": tk.BooleanVar(value=self.config_controller.train_enabled()),
            "trained_model": tk.StringVar(value=self.config_controller.trained_model())
        }

        keyword_frame = tk.LabelFrame(
            self, font=("맑은 고딕", 10, tkFont.BOLD), text="키워드 설정", padx=10
        )
        keyword_frame.pack(anchor=tk.NW)

        tk.Label(keyword_frame, text="포함 키워드").pack(anchor=tk.NW, pady=2)
        tk.Entry(
            keyword_frame, textvariable=self.configs["keywords_to_include"], width=55
        ).pack(anchor=tk.NW, pady=(0, 5))

        tk.Label(keyword_frame, text="제외 키워드").pack(anchor=tk.NW, pady=2)
        tk.Entry(
            keyword_frame, textvariable=self.configs["keywords_to_exclude"], width=55
        ).pack(anchor=tk.NW, pady=(0, 10))

        fasttext_frame = tk.LabelFrame(
            self, font=("맑은 고딕", 10, tkFont.BOLD), text="fastText 설정", padx=10
        )
        fasttext_frame.pack(anchor=tk.NW, pady=(10, 0))

        tk.Label(fasttext_frame, text="fastText 모델 경로").pack(anchor=tk.NW, pady=2)
        browse_frame = tk.Frame(fasttext_frame)
        browse_frame.pack(anchor=tk.NW, fill=tk.BOTH, pady=(0, 10))
        tk.Entry(
            browse_frame,
            readonlybackground="white",
            state="readonly",
            textvariable=self.configs["fasttext_path"],
            width=50
        ).pack(anchor=tk.NW, side=tk.LEFT)
        tk.Button(
            browse_frame,
            command=self.browse_clicked,
            font=("맑은 고딕", 6, tkFont.BOLD),
            text=". . .",
            width=3
        ).pack(anchor=tk.NE, side=tk.RIGHT)

        tk.Checkbutton(
            fasttext_frame,
            command=self.check_button_clicked,
            text="모델 학습 활성화 (모델 이름)",
            variable=self.configs["train_enabled"]
        ).pack(anchor=tk.NW)
        self.trained_model_entry = tk.Entry(
            fasttext_frame,
            state=tk.NORMAL if self.configs["train_enabled"].get() else tk.DISABLED,
            textvariable=self.configs["trained_model"],
            width=55
        )
        self.trained_model_entry.pack(anchor=tk.NW, pady=(0, 10))

        self.focus_set()

    def save_clicked(self):
        """Save configurations.
        """

        self.config_controller.save()
        self.destroy()

    def browse_clicked(self):
        """Browse pretrained fastText model path.
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
