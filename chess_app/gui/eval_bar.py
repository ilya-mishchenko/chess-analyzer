from chess_analyzer.chess_app.constants import EVAL_BAR_HEIGHT, EVAL_BAR_WIDTH
import tkinter as tk
import chess


class EvalBar(tk.Canvas):
    def __init__(self, parent, app):
        super().__init__(parent, height=EVAL_BAR_HEIGHT, width=EVAL_BAR_WIDTH)
        self.app = app
        self.draw_start_pos()

    def draw_start_pos(self):
        self.delete("bar")
        self.create_rectangle(0, 0, 50, 400, fill="black", outline="black", tags="bar")
        self.create_rectangle(
            0, 400, 50, 800, fill="white", outline="black", tags="bar"
        )

    def update_eval(self, value, is_mate, is_draw=False):
        self.delete("bar")

        # ---------------- DRAW ----------------
        if is_draw:
            self.app.eval_score_label.config(text=self.app.state.result)
            self._draw(400)
            return

        # ---------------- РЕАЛЬНЫЙ МАТ (доска в мате) ----------------
        if self.app.state.board.is_checkmate():
            # Определяем победителя
            if self.app.state.board.turn == chess.WHITE:
                # Белые должны ходить, но не могут -> победили чёрные
                self.app.eval_score_label.config(text="Black wins")
                self._draw(800)  # полностью чёрный
            else:
                # Чёрные должны ходить, но не могут -> победили белые
                self.app.eval_score_label.config(text="White wins")
                self._draw(0)  # полностью белый
            return

        # ---------------- МАТОВАЯ УГРОЗА (движок предсказывает мат) ----------------
        if is_mate and not self.app.state.board.is_checkmate():
            mate_in = value if value is not None else 0
            self.app.eval_score_label.config(text=f"M{abs(mate_in)}")

            # Показываем как обычную оценку, но с текстом M
            # mate_in > 0 = белые ставят мат = перевес белых
            # mate_in < 0 = чёрные ставят мат = перевес чёрных
            if mate_in > 0:
                # Перевес белых -> бар стремится к полностью белому
                numeric = 8  # максимальный перевес
            elif mate_in < 0:
                # Перевес чёрных -> бар стремится к полностью чёрному
                numeric = -8
            else:
                numeric = 0

            y = 400 - (numeric * 50)
            y = max(0, min(800, y))
            self._draw(y)
            return

        # ---------------- ОБЫЧНАЯ ПОЗИЦИЯ ----------------
        numeric = max(-8, min(8, value if value is not None else 0))
        self.app.eval_score_label.config(text=f"{numeric:+.2f}")

        y = 400 - (numeric * 50)
        y = max(0, min(800, y))

        self._draw(y)

    def _draw(self, y):
        # y = граница: сверху чёрный, снизу белый
        self.create_rectangle(0, 0, 50, y, fill="black", tags="bar")
        self.create_rectangle(0, y, 50, 800, fill="white", tags="bar")
