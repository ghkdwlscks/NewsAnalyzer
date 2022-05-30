"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import threading
import tkinter as tk
import tkinter.messagebox as tkMessageBox


class NewsButtonView(tk.Frame):
    """NewsButtonView object.

    Args:
        parent (NewsAnalyzer): NewsAnalyzer object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.news_controller = None
        self.config_controller = None

        self.buttons = {
            "load": tk.Button(
                self, command=self.load_model_clicked, takefocus=tk.FALSE, text="모델 불러오기", width=22
            ),
            "run": tk.Button(
                self,
                command=self.run_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="실행",
                width=22
            ),
            "cancel": tk.Button(
                self,
                command=self.cancel_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="취소",
                width=22
            ),
            "add": tk.Button(
                self,
                command=self.add_clicked,
                takefocus=tk.FALSE,
                state=tk.DISABLED,
                text="목록에 추가",
                width=22
            ),
            "open": tk.Button(
                self,
                command=self.open_clicked,
                takefocus=tk.FALSE,
                state=tk.DISABLED,
                text="외부 브라우저에서 열기",
                width=22
            ),
            "config": tk.Button(
                self, command=self.config_clicked, takefocus=tk.FALSE, text="설정", width=22
            ),
            "exit": tk.Button(
                self, command=self.exit_clicked, takefocus=tk.FALSE, text="종료", width=22
            ),
            "text": tk.Button(
                self,
                command=self.text_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="문자보고양식 저장",
                width=22
            ),
            "delete": tk.Button(
                self,
                command=self.delete_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="삭제",
                width=22
            )
        }

        self.buttons["load"].pack(anchor=tk.NW, pady=(30, 10))
        self.buttons["run"].pack(anchor=tk.NW, pady=2)
        self.buttons["cancel"].pack(anchor=tk.NW, pady=(2, 30))
        self.buttons["add"].pack(anchor=tk.NW, pady=2)
        self.buttons["open"].pack(anchor=tk.NW, pady=2)
        self.buttons["config"].pack(anchor=tk.NW, pady=(30, 2))
        self.buttons["exit"].pack(anchor=tk.NW, pady=(30, 50))
        self.buttons["delete"].pack(anchor=tk.SW, pady=(2, 95), side=tk.BOTTOM)
        self.buttons["text"].pack(anchor=tk.SW, pady=(2, 30), side=tk.BOTTOM)

        self.stop_signal = False

        self.run_labels = []

    def set_controllers(self, news_controller, config_controller):
        """Set controllers.

        Args:
            news_controller (NewsController): NewsController object.
            config_controller (ConfigController): ConfigController object.
        """

        self.news_controller = news_controller
        self.config_controller = config_controller

    def load_model_clicked(self):
        """Load pretrained FastText model.
        """

        self.buttons["load"]["state"] = tk.DISABLED
        self.buttons["load"]["text"] = "모델 불러오는 중..."
        self.buttons["config"]["state"] = tk.DISABLED

        threading.Thread(
            target=self.news_controller.load_fasttext_model,
            daemon=True
        ).start()

    def run_clicked(self):
        """Get the number of pages to be crawled.
        """

        run_window = tk.Toplevel(self, padx=10, pady=10)
        run_window.title("Run Configurations")
        run_window.resizable(False, False)
        run_window.geometry(f"+{self.parent.winfo_x() + 365}+{self.parent.winfo_y() + 90}")

        tk.Label(
            run_window, text="가져올 페이지의 수를 입력하세요. (1-400)"
        ).pack(pady=(0, 5))

        num_pages = tk.StringVar()

        tk.Button(
            run_window,
            command=lambda: self.confirm_clicked(run_window, num_pages),
            text="확인"
        ).pack(side=tk.RIGHT)

        input_entry = tk.Entry(run_window, textvariable=num_pages, width=5)
        input_entry.pack(padx=5, side=tk.RIGHT)
        input_entry.focus_set()

        run_window.bind("<Return>", lambda event: self.confirm_clicked(run_window, num_pages))

    def confirm_clicked(self, run_window, num_pages):
        """Pass the number of pages to be crawled to the controller.

        Args:
            run_window (tkinter.Toplevel): Run configurations window.
            num_pages (tkinter.IntVar): Number of pages to be crawled.
        """

        try:
            if int(num_pages.get()) not in range(1, 401):
                raise ValueError
            self.buttons["run"]["state"] = tk.DISABLED
            self.buttons["config"]["state"] = tk.DISABLED
            self.stop_signal = False
            threading.Thread(
                target=self.news_controller.run,
                args=(int(num_pages.get()), lambda: self.stop_signal),
                daemon=True
            ).start()
            run_window.destroy()
        except ValueError:
            tkMessageBox.showerror("Error", "1-400 사이의 수를 입력하세요!", parent=run_window)

    def cancel_clicked(self):
        """Set stop signal.
        """

        self.stop_signal = True

    def add_clicked(self):
        """Add selected article to selection list.
        """

        self.news_controller.add_to_list()

    def open_clicked(self):
        """Open selected article in external browser.
        """

        self.news_controller.open_article()

    def config_clicked(self):
        """Open configuration window.
        """

        def update_load_button(old_model, new_model):
            if old_model == new_model:
                self.buttons["load"]["state"] = tk.DISABLED
                self.buttons["load"]["text"] = "Model loaded!"
                self.buttons["run"]["state"] = tk.NORMAL
            elif old_model:
                self.buttons["load"]["state"] = tk.NORMAL
                self.buttons["load"]["text"] = "Reload model"
                self.buttons["run"]["state"] = tk.DISABLED

        self.config_controller.config_clicked(
            self, self.news_controller.lastest_fasttext_model, update_load_button
        )

    def exit_clicked(self):
        """Exit Program.
        """

        self.parent.parent.destroy()

    def text_clicked(self):
        """Export text format.
        """

        self.news_controller.export_text_format()

    def delete_clicked(self):
        """Delete selected article from selection list.
        """

        self.news_controller.delete_from_list()
