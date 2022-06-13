"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import threading
import tkinter as tk
import tkinter.messagebox as tkMessageBox

import pandastable as pt


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
                self, command=self.run_clicked, takefocus=tk.FALSE, text="실행", width=22
            ),
            "cancel": tk.Button(
                self,
                command=self.cancel_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="취소",
                width=22
            ),
            "add_to_blacklist": tk.Button(
                self,
                command=self.add_to_blacklist_clicked,
                state=tk.DISABLED,
                takefocus=tk.FALSE,
                text="블랙리스트에 추가",
                width=22
            ),
            "open_blacklist": tk.Button(
                self,
                command=self.open_blacklist_clicked,
                takefocus=tk.FALSE,
                text="블랙리스트 열기",
                width=22
            ),
            "exit": tk.Button(
                self, command=self.exit_clicked, takefocus=tk.FALSE, text="종료", width=22
            )
        }

        self.buttons["run"].pack(anchor=tk.NW, pady=(30, 2))
        self.buttons["cancel"].pack(anchor=tk.NW, pady=2)
        self.buttons["add_to_blacklist"].pack(anchor=tk.NW, pady=(30, 2))
        self.buttons["open_blacklist"].pack(anchor=tk.NW, pady=2)
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
            run_window, text="가져올 페이지의 수를 입력하세요. (1-100)"
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
            if int(num_pages.get()) not in range(1, 101):
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
            tkMessageBox.showerror("Error", "1-100 사이의 수를 입력하세요!", parent=run_window)

    def cancel_clicked(self):
        """Set stop signal.
        """

        self.stop_signal = True

    def add_to_blacklist_clicked(self):
        """Add to blacklist.
        """

        self.market_controller.add_to_blacklist()

    def open_blacklist_clicked(self):
        """Open blacklist.
        """

        blacklist_window = tk.Toplevel(self, padx=10 ,pady=10)
        blacklist_window.title("Blacklist")
        blacklist_window.resizable(False, False)
        blacklist_window.geometry(f"+{self.parent.winfo_x() + 365}+{self.parent.winfo_y() + 90}")

        table_frame = tk.Frame(blacklist_window)
        table_frame.pack(expand=tk.TRUE, fill=tk.BOTH, padx=10, pady=10, side=tk.LEFT)

        table = pt.Table(
            table_frame,
            dataframe=self.market_controller.blacklist.dataframe,
            width=660,
            editable=False,
            thefont=("맑은 고딕", 11),
            cellwidth=150
        )
        table.setSelectedRow(-1)

        def on_closing():
            self.unbind_all("<Return>")
            blacklist_window.destroy()

        blacklist_window.protocol("WM_DELETE_WINDOW", on_closing)

        button_frame = tk.Frame(blacklist_window)
        button_frame.pack(fill=tk.BOTH, padx=10, pady=10, side=tk.RIGHT)

        insert_button = tk.Button(button_frame, text="추가", width=12)
        insert_button.pack(anchor=tk.NW, pady=(25, 2))

        def on_delete(delete_button):
            table.deleteRow()
            delete_button["state"] = tk.DISABLED if table.getSelectedRow() < 0 else tk.NORMAL

        delete_button = tk.Button(
            button_frame,
            command=lambda: on_delete(delete_button),
            state=tk.DISABLED,
            text="삭제",
            width=12
        )
        delete_button.pack(anchor=tk.NW, pady=2)

        def on_click(event):
            table.handle_left_click(event)
            delete_button["state"] = tk.DISABLED if table.getSelectedRow() < 0 else tk.NORMAL

        table.bind("<Button-1>", on_click)

        def on_save():
            self.market_controller.blacklist.dataframe = table.model.df
            self.market_controller.blacklist.save()
            on_closing()

        save_button = tk.Button(button_frame, command=on_save, text="저장", width=12)
        save_button.pack(anchor=tk.NW, pady=25)

        table.show()

    def exit_clicked(self):
        """Exit Program.
        """

        self.parent.parent.destroy()
