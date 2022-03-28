"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import threading
import tkinter as tk
import tkinter.messagebox as tkMessageBox


class MarketButtonView(tk.Frame):
    """MarketButtonView object.

    Args:
        parent (MarcketWatcher): MarcketWatcher object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.market_controller = None

        self.buttons = {
            "run": tk.Button(
                self,
                command=self.run_clicked,
                takefocus=tk.FALSE,
                text="Run",
                width=22
            ),
            "cancel": tk.Button(
                self,
                command=self.cancel_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="Cancel",
                width=22
            ),
            "exit": tk.Button(
                self, command=self.exit_clicked, takefocus=tk.FALSE, text="Exit", width=22
            )
        }

        self.buttons["run"].pack(anchor=tk.NW, pady=(30, 2))
        self.buttons["cancel"].pack(anchor=tk.NW, pady=2)
        self.buttons["exit"].pack(anchor=tk.NW, pady=(30, 50))

        self.stop_signal = False

    def set_controller(self, market_controller):
        """Set controller.

        Args:
            market_controller (MarketController): MarketController object.
        """

        self.market_controller = market_controller

    def run_clicked(self):
        """Get the number of pages to be crawled.
        """

        run_window = tk.Toplevel(self, padx=10, pady=10)
        run_window.title("Run Configurations")
        run_window.resizable(False, False)
        run_window.geometry(f"+{self.parent.winfo_x() + 365}+{self.parent.winfo_y() + 90}")

        tk.Label(
            run_window, text="Input the number of pages to be crawled. (1-1000)"
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
            if int(num_pages.get()) not in range(1, 1001):
                raise ValueError
            self.buttons["run"]["state"] = tk.DISABLED
            self.stop_signal = False
            threading.Thread(
                target=self.market_controller.run,
                args=(int(num_pages.get()), lambda: self.stop_signal),
                daemon=True
            ).start()
            run_window.destroy()
        except ValueError:
            tkMessageBox.showerror("Error", "Input should be 1-1000!", parent=run_window)

    def cancel_clicked(self):
        """Set stop signal.
        """

        self.stop_signal = True

    def exit_clicked(self):
        """Exit Program.
        """

        self.parent.parent.destroy()
