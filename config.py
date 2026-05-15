import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ICON = BASE_DIR / "assets" / "app_icon.png"

PIECES_DIR = BASE_DIR / "assets" / "pieces"
MOVE_ICONS_DIR = BASE_DIR / "assets" / "move_classify"

STOCKFISH_PATH = Path(
    os.getenv("STOCKFISH_PATH", BASE_DIR / "engine" / "stockfish" / "stockfish.exe")
)
