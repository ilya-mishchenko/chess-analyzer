from PIL import Image, ImageTk

from chess_analyzer.config import PIECES_DIR, MOVE_ICONS_DIR

PIECE_FILES = {
    "P": "wP.png",
    "N": "wN.png",
    "B": "wB.png",
    "R": "wR.png",
    "Q": "wQ.png",
    "K": "wK.png",
    "p": "bP.png",
    "n": "bN.png",
    "b": "bB.png",
    "r": "bR.png",
    "q": "bQ.png",
    "k": "bK.png",
}

MOVE_ICONS_FILES = {
    "strong": "strong.png",
    "best": "engine_best.png",
    "inaccuracy": "inaccuracy.png",
    "mistake": "mistake.png",
    "blunder": "blunder.png",
    "good": "good.png",
}


def load_piece_images(square_size: int):
    pieces = {}

    for symbol, filename in PIECE_FILES.items():
        image_path = PIECES_DIR / filename
        image = Image.open(image_path)
        image = image.resize((square_size, square_size))

        pieces[symbol] = ImageTk.PhotoImage(image)

    return pieces


def load_move_icons(size: int):
    icons = {}

    for symbol, filename in MOVE_ICONS_FILES.items():
        image_path = MOVE_ICONS_DIR / filename
        image = Image.open(image_path)
        image = image.resize((size, size))

        icons[symbol] = ImageTk.PhotoImage(image)

    return icons
