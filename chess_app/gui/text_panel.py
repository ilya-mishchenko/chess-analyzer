import tkinter as tk
from tkinter import ttk


class TextPanel(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.pgn_text = tk.Text(self, width=100, height=30)
        self.pgn_text.pack()

        self.load_pgn_button = ttk.Button(
            self, text="Load game", command=self.app.load_game
        )
        self.load_pgn_button.pack(pady=(10, 10))

        self.adjust_depth_box = ttk.Spinbox(self, state="readonly", from_=5, to=25)
        self.adjust_depth_box.pack(pady=(50, 10))

        self.update_depth_button = ttk.Button(
            self, text="Update depth", command=self.up_depth
        )
        self.update_depth_button.pack(pady=(10, 10))

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Вставить", command=self.paste_text)

        self.pgn_text.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def paste_text(self):
        try:
            text = self.clipboard_get()
            self.pgn_text.insert(tk.INSERT, text)

        except tk.TclError:
            pass

    def set_current_move(self, text):
        self.cur_move_label.config(text=text)

    def up_depth(self):
        new_depth = self.adjust_depth_box.get()
        self.app.engine_service.update_depth(new_depth)
