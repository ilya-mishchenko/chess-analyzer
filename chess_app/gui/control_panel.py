from tkinter import ttk


class ControlPanel(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=25)

        self.app = app

        self.button_show_best_move = ttk.Button(
            self,
            text="Show best move",
            command=self.app.show_best_move,
            state="disabled",
        )

        self.button_show_best_move.pack(side="top", pady=10)

        self.button_next_move = ttk.Button(
            self, text="Next move", command=self.app.next_move, state="disabled"
        )

        self.button_next_move.pack(side="right", padx=(10, 0))

        self.button_prev_move = ttk.Button(
            self,
            text="Previous move",
            command=self.app.prev_move,
            state="disabled",
        )

        self.button_prev_move.pack(side="left", padx=(0, 10))

    def enable_buttons(self):
        self.button_next_move.config(state="normal")
        self.button_prev_move.config(state="normal")
        self.button_show_best_move.config(state="normal")
