"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
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

        self.load_model_button = tk.Button(
            self, command=self.load_model_clicked, text="Load model", width=22
        )
        self.load_model_button.pack(anchor=tk.NE, pady=(30, 2))

        self.run_button = tk.Button(
            self, command=self.run_clicked, state=tk.DISABLED, text="Run", width=22
        )
        self.run_button.pack(anchor=tk.NE, pady=(2, 5))

        self.config_button = tk.Button(
            self, command=self.config_clicked, text="Configurations", width=22
        )
        self.config_button.pack(anchor=tk.SE, pady=2, side=tk.BOTTOM)

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

        self.load_model_button["state"] = tk.DISABLED
        self.load_model_button["text"] = "Loading model..."
        self.config_button["state"] = tk.DISABLED

        threading.Thread(
            target=self.main_controller.load_fasttext_model,
            args=[self.config_controller.fasttext_path()],
            daemon=True
        ).start()

    def run_clicked(self):
        """Get the number of pages to be crawled.
        """

        run_window = tk.Toplevel(self, padx=10, pady=10)
        run_window.title("Run Configurations")
        run_window.geometry(f"+{self.parent.winfo_x() + 400}+{self.parent.winfo_y() + 90}")

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
            self.run_button["state"] = tk.DISABLED
            self.config_button["state"] = tk.DISABLED
            threading.Thread(
                target=self.main_controller.run,
                args=[
                    int(num_pages.get()),
                    self.config_controller.keywords_to_include(),
                    self.config_controller.keywords_to_exclude()
                ],
                daemon=True
            ).start()
            run_window.destroy()
        except ValueError:
            tkMessageBox.showerror("Error", "Input should be 1-400!", parent=run_window)

    def config_clicked(self):
        """Open configuration window.
        """

        self.config_controller.config_clicked(self)
