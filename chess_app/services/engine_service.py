import chess.engine
from chess_analyzer.config import STOCKFISH_PATH


class EngineService:
    def __init__(self, depth=16, threads=1):
        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(
            str(STOCKFISH_PATH),
            setpgrp=False,
        )

        self.engine.configure(
            {
                "Threads": threads,
                "Hash": 16,
            }
        )

    def analyze_position(self, board):
        # ---------------- DRAW STATES ----------------
        if board.is_stalemate():
            return self._draw_result("Stalemate")

        if board.is_insufficient_material():
            return self._draw_result("Insufficient material")

        if board.can_claim_threefold_repetition():
            return self._draw_result("Threefold repetition")

        if board.can_claim_fifty_moves():
            return self._draw_result("50-move rule")

        # ---------------- ENGINE ----------------

        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))

        pv = info.get("pv", [])
        best_move = pv[0] if pv else None

        score_obj = info["score"].white()

        is_mate = score_obj.is_mate()
        mate_in = score_obj.mate() if is_mate else None

        evaluation = None if is_mate else score_obj.score() / 100

        winner = None
        if board.is_checkmate():
            winner = not board.turn

        return {
            "best_move": best_move,
            "evaluation": evaluation,
            "is_mate": is_mate,
            "mate_in": mate_in,
            "is_draw": False,
            "result": None,
            "winner": winner,
        }

    def _draw_result(self, reason):
        return {
            "best_move": None,
            "evaluation": 0.0,
            "is_mate": False,
            "mate_in": None,
            "is_draw": True,
            "result": reason,
            "winner": None,
        }

    def quit(self):
        self.engine.quit()
