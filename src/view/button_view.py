"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import threading
import tkinter as tk
import tkinter.messagebox as tkMessageBox


class ButtonView(tk.Frame):
    """ButtonView object.

    Args:
        parent (NewsAnalyzer): NewsAnalyzer object.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.main_controller = None
        self.config_controller = None

        self.buttons = {
            "load": tk.Button(
                self, command=self.load_model_clicked, text="Load model", width=22
            ),
            "run": tk.Button(
                self, command=self.run_clicked, state=tk.DISABLED, text="Run", width=22
            ),
            "cancel": tk.Button(
                self, command=self.cancel_clicked, state=tk.DISABLED, text="Cancel", width=22
            ),
            "config": tk.Button(
                self, command=self.config_clicked, text="Configurations", width=22
            )
        }

        self.buttons["load"].pack(anchor=tk.NE, pady=(30, 10))
        self.buttons["run"].pack(anchor=tk.NE, pady=2)
        self.buttons["cancel"].pack(anchor=tk.NE, pady=(2, 5))
        self.buttons["config"].pack(anchor=tk.SE, pady=2, side=tk.BOTTOM)

        self.stop_signal = False

        self.run_labels = []

    def set_controllers(self, main_controller, config_controller):
        """Set controllers.

        Args:
            main_controller (MainController): MainController object.
            config_controller (ConfigController): ConfigController object.
        """

        self.main_controller = main_controller
        self.config_controller = config_controller

    def load_model_clicked(self):
        """Load pretrained FastText model.
        """

        self.buttons["load"]["state"] = tk.DISABLED
        self.buttons["load"]["text"] = "Loading model..."
        self.buttons["config"]["state"] = tk.DISABLED

        threading.Thread(
            target=self.main_controller.load_fasttext_model,
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
            run_window, text="Input the number of pages to be crawled. (1-400)"
        ).pack(pady=(0, 5))

        num_pages = tk.StringVar()

        tk.Button(
            run_window,
            command=lambda: self.confirm_clicked(run_window, num_pages),
            text="Confirm"
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
                target=self.main_controller.run,
                args=[int(num_pages.get()), lambda: self.stop_signal],
                daemon=True
            ).start()
            run_window.destroy()
        except ValueError:
            tkMessageBox.showerror("Error", "Input should be 1-400!", parent=run_window)

    def cancel_clicked(self):
        """Set stop signal.
        """

        self.stop_signal = True

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
            self, self.main_controller.lastest_fasttext_model, update_load_button
        )
