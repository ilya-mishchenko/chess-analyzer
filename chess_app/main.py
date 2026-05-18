import tkinter as tk
from chess_analyzer.chess_app.gui.main_window import ChessApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
