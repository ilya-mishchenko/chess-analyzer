import io
import chess
import chess.pgn


def load_pgn(pgn_text: str):
    game = chess.pgn.read_game(io.StringIO(pgn_text))

    if game is None:
        return None, None, None

    board = game.board()
    moves = list(game.mainline_moves())

    if not moves:
        return None, None, None

    san_moves = []
    temp_board = board.copy()

    for move in moves:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)

    return board, moves, san_moves
