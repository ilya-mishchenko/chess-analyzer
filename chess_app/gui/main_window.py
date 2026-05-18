import ttkbootstrap as ttkb
from tkinter import ttk
import tkinter as tk

from chess_analyzer.config import ICON
from chess_analyzer.chess_app.constants import WINDOW_RES
from chess_analyzer.chess_app.gui.board_canvas import BoardCanvas
from chess_analyzer.chess_app.gui.control_panel import ControlPanel
from chess_analyzer.chess_app.gui.eval_bar import EvalBar
from chess_analyzer.chess_app.gui.text_panel import TextPanel

from chess_analyzer.chess_app.services.engine_service import EngineService
from chess_analyzer.chess_app.services.image_loader import (
    load_piece_images,
    load_move_icons,
)
from chess_analyzer.chess_app.services.move_scorer import classify_move
from chess_analyzer.chess_app.services.pgn_service import load_pgn
from chess_analyzer.chess_app.services.game_state import GameState


class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChessAnalyze")
        self.root.geometry(WINDOW_RES)

        icon = tk.PhotoImage(file=ICON)
        self.root.iconphoto(True, icon)

        self.style = ttkb.Style()
        self.style.theme_use("darkly")

        self.root.grid_columnconfigure(0, minsize=150)
        self.root.grid_rowconfigure(0, minsize=150)

        self.status_pgn_label = ttk.Label(root, text="")
        self.status_pgn_label.grid(row=2, column=2)

        self.button_quit = ttk.Button(root, text="QUIT", command=self.quit_app)
        self.button_quit.grid(row=2, column=1)

        self.eval_score_label = ttk.Label(root, text="")
        self.eval_score_label.grid(row=3, column=0)

        self.control_panel = ControlPanel(parent=self.root, app=self)
        self.control_panel.grid(row=1, column=1)

        self.text_panel = TextPanel(parent=self.root, app=self)
        self.text_panel.grid(row=0, column=2, sticky="n")

        self.board_canvas = BoardCanvas(parent=self.root, app=self)
        self.board_canvas.grid(row=0, column=1)

        self.eval_bar = EvalBar(parent=self.root, app=self)
        self.eval_bar.grid(row=0, column=0)

        self.engine_service = EngineService()
        self.state = GameState()

        self.pieces = load_piece_images(100)
        self.move_icons = load_move_icons(25)

        self.update_engine_info()

    # ---------------- ENGINE ----------------

    def update_engine_info(self):
        result = self.engine_service.analyze_position(self.state.board)
        self.state.update_engine(result)

    # ---------------- RENDER ----------------

    def render(self):
        self.board_canvas.redraw_board(self.state.board)

        if self.state.last_move and self.state.last_classification not in (
            "good",
            None,
        ):
            self.board_canvas.draw_move_icon(
                self.state.last_move,
                self.state.last_classification,
            )

        self.eval_bar.update_eval(
            self.state.mate_in if self.state.is_mate else self.state.eval_value,
            is_mate=self.state.is_mate,
            is_draw=self.state.is_draw,
        )

    # ---------------- LOAD GAME ----------------

    def load_game(self):
        pgn_text = self.text_panel.pgn_text.get("1.0", tk.END).strip()

        board, moves, san_moves = load_pgn(pgn_text)

        if board is None:
            self.status_pgn_label.config(text="PGN error")
            return
        self.status_pgn_label.config(text="Game loaded")
        self.state.board = board
        self.state.moves = moves
        self.state.moves_san = san_moves
        self.state.current_move = 0
        self.state.move_classifications.clear()

        self.state.last_move = None
        self.state.last_classification = None

        self.board_canvas.delete("move_icon")
        self.board_canvas.delete("arrow")

        self.board_canvas.redraw_board(self.state.board)

        self.control_panel.enable_buttons()
        self.update_engine_info()
        self.render()

    # ---------------- NEXT MOVE ----------------

    def next_move(self):
        if self.state.current_move >= len(self.state.moves):
            return

        move = self.state.moves[self.state.current_move]

        # Получаем данные ПЕРЕД ходом
        moved_color = self.state.board.turn
        eval_before = self.state.eval_value
        was_mate_before = self.state.is_mate
        best_before = self.state.best_move

        self.state.apply_move(move)

        result = self.engine_service.analyze_position(self.state.board)
        self.state.update_engine(result)
        self.state.update_position_state()

        classification = classify_move(
            move=move,
            best_move=best_before,
            eval_before=eval_before,
            eval_after=self.state.eval_value,
            moved_color=moved_color,
            was_mate_before=was_mate_before,
            is_mate_after=self.state.is_mate,
        )

        self.state.add_classification(classification)
        self.state.last_move = move
        self.state.last_classification = classification

        self.render()

    # ---------------- PREV MOVE ----------------

    def prev_move(self):
        if self.state.current_move <= 0:
            return

        self.state.revert_move()

        eval_before_data = self.state.get_eval_before_move(self.state.current_move)

        result = self.engine_service.analyze_position(self.state.board)
        self.state.update_engine(result)
        self.state.update_position_state()

        if self.state.current_move > 0:
            self.state.last_move = self.state.moves[self.state.current_move - 1]
            self.state.last_classification = self.state.move_classifications[
                self.state.current_move - 1
            ]
        else:
            self.state.last_move = None
            self.state.last_classification = None

        self.render()

    # ---------------- BEST MOVE ----------------

    def show_best_move(self):
        if self.state.best_move is None:
            return

        self.board_canvas.draw_best_move_arrow(self.state.best_move)

    # ---------------- EXIT ----------------

    def quit_app(self):
        self.engine_service.quit()
        self.root.destroy()
