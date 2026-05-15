import chess


def classify_move(
    move,
    best_move,
    eval_before,
    eval_after,
    moved_color,
    was_mate_before,
    is_mate_after,
):

    if was_mate_before and is_mate_after:
        return "good"

    if not was_mate_before and is_mate_after:

        if best_move is not None and move == best_move:
            return "brilliant"

        return "blunder"

    if was_mate_before and not is_mate_after:
        return "good"

    if eval_before is None:
        eval_before = 0.0

    if eval_after is None:
        eval_after = 0.0

    raw_delta = eval_after - eval_before

    if moved_color == chess.BLACK:
        delta = -raw_delta
    else:
        delta = raw_delta

    if best_move is not None and move == best_move:
        return "best"

    elif delta <= -2.0:
        return "blunder"

    elif delta <= -1.3:
        return "mistake"

    elif delta <= -0.5:
        return "inaccuracy"

    elif delta >= 2:
        return "strong"

    else:
        return None
