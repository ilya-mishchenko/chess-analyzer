## CHESS ANALYZER 

Chess analysis tool 
with Stockfish engine integration 
and GUI for move evaluation and position analysis.

## Features

- Chess position analysis using Stockfish
- Best move suggestion
- Evaluation (centipawns / mate detection)
- Draw detection (stalemate, repetition, 50-move rule)
- GUI interface for board interaction
## Installation

Install dependencies:

```bash
pip install -r requirements.txt

```

### 4. Stockfish Installation (MANUALLY)

```md
## Stockfish setup

Download Stockfish from official website:
https://stockfishchess.org/download/

Place the executable here:
engine/stockfish/stockfish.exe

Or set custom path via environment variable:
STOCKFISH_PATH=/path/to/stockfish
```
## Run

```bash
python chess_app/main.py
```
## Analysis behavior

Position evaluation is performed on-demand each time the user requests analysis (e.g., button press in GUI).

This means:

- Each analysis call triggers a fresh Stockfish search
- Results are not cached by default
- Evaluation may slightly vary between runs depending on search depth, time limit, and engine heuristics
- This is expected behavior for chess engines and does not indicate inconsistency or a bug

## Future improvements

Possible directions for further development:

- Add caching for repeated position evaluations
- Improve move visualization in GUI
- Add analysis depth/time presets for different strength levels