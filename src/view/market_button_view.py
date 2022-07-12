"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import threading
import tkinter as tk
import tkinter.messagebox as tkMessageBox

import pandastable as pt

from model.market_post import MarketPost


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

        self.run_labels = []

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

        table_frame = tk.Frame(blacklist_window)
        table_frame.pack(expand=tk.TRUE, fill=tk.BOTH, padx=(0, 20), side=tk.LEFT)

        table = pt.Table(
            table_frame,
            dataframe=self.market_controller.blacklist.dataframe,
            width=660,
            editable=False,
            thefont=("맑은 고딕", 11),
            cellwidth=150
        )
        table.setSelectedRow(-1)
        table.unbind_all("<Return>")
        table.unbind_all("<Tab>")

        def on_closing():
            blacklist_window.destroy()

        blacklist_window.protocol("WM_DELETE_WINDOW", on_closing)

        button_frame = tk.Frame(blacklist_window)
        button_frame.pack(fill=tk.BOTH, side=tk.RIGHT)

        def on_insert():
            insert_window = tk.Toplevel(blacklist_window, padx=10, pady=10)
            insert_window.title("Insert blacklist")
            insert_window.resizable(False, False)

            tk.Label(insert_window, text="수동으로 블랙리스트에 추가합니다.").pack(anchor=tk.W, pady=(0, 5))

            nickname = tk.StringVar()
            email = tk.StringVar()
            phone = tk.StringVar()

            entry_frame = tk.Frame(insert_window)
            entry_frame.pack(fill=tk.BOTH, padx=(0, 10), side=tk.LEFT)

            nickname_frame = tk.Frame(entry_frame)
            nickname_frame.pack(fill=tk.BOTH)
            tk.Label(nickname_frame, text="닉네임").pack(side=tk.LEFT)
            nickname_entry = tk.Entry(nickname_frame, textvariable=nickname, width=20)
            nickname_entry.pack(padx=5, side=tk.RIGHT)

            email_frame = tk.Frame(entry_frame)
            email_frame.pack(fill=tk.BOTH)
            tk.Label(email_frame, text="이메일").pack(side=tk.LEFT)
            tk.Entry(email_frame, textvariable=email, width=20).pack(padx=5, side=tk.RIGHT)

            phone_frame = tk.Frame(entry_frame)
            phone_frame.pack(fill=tk.BOTH)
            tk.Label(phone_frame, text="휴대폰").pack(side=tk.LEFT)
            tk.Entry(phone_frame, textvariable=phone, width=20).pack(padx=5, side=tk.RIGHT)

            def on_confirm():
                if nickname.get() or email.get() or phone.get():
                    self.market_controller.add_to_blacklist(
                        MarketPost(None, None, nickname.get(), email.get(), phone.get(), None)
                    )
                    table.updateModel(pt.TableModel(self.market_controller.blacklist.dataframe))
                    table.redraw()
                insert_window.destroy()

            tk.Button(
                insert_window, command=on_confirm, text="확인", width=8
            ).pack(anchor=tk.NW, pady=2)

            def on_cancel():
                insert_window.destroy()

            tk.Button(
                insert_window, command=on_cancel, text="취소", width=8
            ).pack(anchor=tk.NW, pady=2)

            nickname_entry.focus_set()

            insert_window.bind("<Return>", lambda event: on_confirm())

        insert_button = tk.Button(button_frame, command=on_insert, text="추가", width=12)
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
