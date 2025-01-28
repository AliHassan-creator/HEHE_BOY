# HEHE_BOY
CHESS Project
---

# Chess Game with Tkinter

This repository contains a fully interactive chess game built using Python and the Tkinter library. The game offers a simple graphical user interface, making it easy to play chess directly on your local machine.

## Features
- **Complete Chess Rules:** Implements standard chess rules, including:
  - Pawn promotion
  - Castling (both kingside and queenside)
  - En passant captures
  - King safety checks (no moves leaving the king in check)
- **Turn-Based Gameplay:** Tracks turns for white and black players.
- **Check and Checkmate Detection:** Alerts players when a king is in check or checkmate.
- **Interactive Board:** Highlights valid moves for selected pieces.
- **Reset Option:** Restart the game at any time by pressing the `r` key.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chess-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd chess-game
   ```
3. Run the script:
   ```bash
   python Chess.py
   ```
   Ensure you have Python installed on your system (tested on Python 3.10).

## Dependencies
- No external dependencies are required. The script uses Python's built-in `tkinter` module for the GUI.

## How to Play
- Select a piece by clicking on it.
- Valid moves will be highlighted on the board.
- Click on a highlighted square to move the piece.
- Special moves, like castling and en passant, are supported.
- If a pawn reaches the opposite end of the board, you'll be prompted to promote it to a piece of your choice.

## Screenshot
<img width="231" alt="image" src="https://github.com/user-attachments/assets/1c282751-bdac-4789-a4d8-aa4c55c96ff3" />

Feel free to adjust the repository URL or add screenshots as necessary!
