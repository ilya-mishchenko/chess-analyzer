import chess


class GameState:
    def __init__(self):
        self.board = chess.Board()

        self.moves = []
        self.moves_san = []
        self.current_move = 0

        self.move_classifications = []

        self.evals_before_move = []
        self.best_moves_before = []
        self.mate_before = []

        self.eval_value = 0.0
        self.is_mate = False
        self.mate_in = None
        self.best_move = None
        self.last_move = None
        self.last_classification = None

        self.prev_eval = 0.0
        self.was_mate = False

        self.is_draw = False
        self.result = None
        self.winner = None
        self.display = ""

    def apply_move(self, move):
        self.evals_before_move.append(
            {
                "eval": self.eval_value,
                "best_move": self.best_move,
                "is_mate": self.is_mate,
                "mate_in": self.mate_in,
            }
        )

        self.board.push(move)
        self.current_move += 1

    def revert_move(self):
        self.board.pop()
        self.current_move -= 1

        if self.evals_before_move:
            self.evals_before_move.pop()
        if self.move_classifications:
            self.move_classifications.pop()

    def get_eval_before_move(self, move_index):
        if move_index < len(self.evals_before_move):
            return self.evals_before_move[move_index]
        return None

    def update_engine(self, result: dict):
        self.prev_eval = self.eval_value
        self.was_mate = self.is_mate

        self.best_move = result["best_move"]
        self.is_mate = result["is_mate"]
        self.mate_in = result["mate_in"]
        self.is_draw = result["is_draw"]
        self.result = result["result"]

        self.eval_value = result["evaluation"]

        if result["is_mate"]:
            self.display = f"M{result['mate_in']}"
        else:
            self.display = f"{result['evaluation']:+.2f}"

    def add_classification(self, classification):
        self.move_classifications.append(classification)

    def snapshot(self):
        return {
            "board": self.board.copy(),
            "current_move": self.current_move,
            "eval_value": self.eval_value,
            "is_mate": self.is_mate,
            "mate_in": self.mate_in,
            "best_move": self.best_move,
        }

    def update_position_state(self):
        self.winner = None

        if self.board.is_checkmate():
            self.winner = not self.board.turn

        elif self.board.is_stalemate():
            self.winner = None

        elif self.board.is_insufficient_material():
            self.winner = None
