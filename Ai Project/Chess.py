import tkinter as tk
from tkinter import simpledialog, messagebox, Tk, Button
import random


root = tk.Tk()
root.title("Chess Board")
root.geometry("640x640")
root.configure(bg="grey")

white_king_moved = False
white_rook_king_side_moved = False
white_rook_queen_side_moved = False
black_king_moved = False
black_rook_king_side_moved = False
black_rook_queen_side_moved = False
last_move = None 


white_pieces = {
    "Pawn": "\u2659",
    "Rook": "\u2656",
    "Knight": "\u2658",
    "Bishop": "\u2657",
    "Queen": "\u2655",
    "King": "\u2654",
}

black_pieces = {
    "Pawn": "\u265F",
    "Rook": "\u265C",
    "Knight": "\u265E",
    "Bishop": "\u265D",
    "Queen": "\u265B",
    "King": "\u265A",
}

# Initial board setup
board = [
    [black_pieces["Rook"], black_pieces["Knight"], black_pieces["Bishop"], black_pieces["Queen"],
     black_pieces["King"], black_pieces["Bishop"], black_pieces["Knight"], black_pieces["Rook"]],
    [black_pieces["Pawn"]] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [white_pieces["Pawn"]] * 8,
    [white_pieces["Rook"], white_pieces["Knight"], white_pieces["Bishop"], white_pieces["Queen"],
     white_pieces["King"], white_pieces["Bishop"], white_pieces["Knight"], white_pieces["Rook"]],
]

# Colors for the chessboard squares
light_square = "#ACD123"  
dark_square = "#A1A1A1"   


# Creating the frame for the chessboard
board_frame = tk.Frame(root)
board_frame.pack(expand=True)

# Tracking selected piece and position
selected_piece = None
selected_pos = None

turn = "white"  # Track whose turn it is

# Function to get valid moves for the Pawn piece
def get_moves_for_pawn(row, col, is_white):
    moves = []
    direction = -1 if is_white else 1
    enemy_pieces = black_pieces.values() if is_white else white_pieces.values()

    if 0 <= row + direction < 8:
        # Normal forward movement
        if board[row + direction][col] == "":
            moves.append((row + direction, col))
        # Double move from starting position
        if (row == 6 and is_white or row == 1 and not is_white) and board[row + direction][col] == "" and board[row + 2 * direction][col] == "":
            moves.append((row + 2 * direction, col))
        # Diagonal captures
        if col > 0 and board[row + direction][col - 1] in enemy_pieces:
            moves.append((row + direction, col - 1))
        if col < 7 and board[row + direction][col + 1] in enemy_pieces:
            moves.append((row + direction, col + 1))
            


    return moves



# Function to get valid moves for the Knight piece
def get_moves_for_knight(row, col):
    moves = []
    knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in (white_pieces.values() if board[row][col] in white_pieces.values() else black_pieces.values()):
            moves.append((r, c))
    return moves

# Function to get valid moves for sliding pieces (Rook, Bishop, Queen)
def get_sliding_piece_moves(row, col, directions):
    moves = []
    enemy_pieces = black_pieces.values() if board[row][col] in white_pieces.values() else white_pieces.values()
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "":
                moves.append((r, c))
            elif board[r][c] in enemy_pieces:
                moves.append((r, c))
                break
            else:
                break
            r += dr
            c += dc
    return moves

# Functions to get moves for specific pieces
def get_moves_for_rook(row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return get_sliding_piece_moves(row, col, directions)

def get_moves_for_bishop(row, col):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_sliding_piece_moves(row, col, directions)

def get_moves_for_queen(row, col):
    return get_moves_for_rook(row, col) + get_moves_for_bishop(row, col)

def get_moves_for_king(row, col):
    """Get valid moves for the King, including castling"""
    moves = []
    king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in (white_pieces.values() if board[row][col] in white_pieces.values() else black_pieces.values()):
            moves.append((r, c))

    # Add castling moves if allowed
    is_white = board[row][col] == white_pieces["King"]
    if is_white and not white_king_moved:
        # King-side castling
        if not white_rook_king_side_moved and board[7][5] == "" and board[7][6] == "" and not is_square_attacked(7, 4, True) and not is_square_attacked(7, 5, True) and not is_square_attacked(7, 6, True):
            moves.append((7, 6))
        # Queen-side castling
        if not white_rook_queen_side_moved and board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and not is_square_attacked(7, 4, True) and not is_square_attacked(7, 2, True) and not is_square_attacked(7, 3, True):
            moves.append((7, 2))
    elif not is_white and not black_king_moved:
        # King-side castling
        if not black_rook_king_side_moved and board[0][5] == "" and board[0][6] == "" and not is_square_attacked(0, 4, False) and not is_square_attacked(0, 5, False) and not is_square_attacked(0, 6, False):
            moves.append((0, 6))
        # Queen-side castling
        if not black_rook_queen_side_moved and board[0][1] == "" and board[0][2] == "" and board[0][3] == "" and not is_square_attacked(0, 4, False) and not is_square_attacked(0, 2, False) and not is_square_attacked(0, 3, False):
            moves.append((0, 2))

    return moves

def highlight_moves(row, col):
    piece = board[row][col]
    moves = []

    if piece in (white_pieces["Pawn"], black_pieces["Pawn"]):
        moves = get_moves_for_pawn(row, col, piece in white_pieces.values())
    elif piece in (white_pieces["Knight"], black_pieces["Knight"]):
        moves = get_moves_for_knight(row, col)
    elif piece in (white_pieces["Rook"], black_pieces["Rook"]):
        moves = get_moves_for_rook(row, col)
    elif piece in (white_pieces["Bishop"], black_pieces["Bishop"]):
        moves = get_moves_for_bishop(row, col)
    elif piece in (white_pieces["Queen"], black_pieces["Queen"]):
        moves = get_moves_for_queen(row, col)
    elif piece in (white_pieces["King"], black_pieces["King"]):
        moves = get_moves_for_king(row, col)

    for r, c in moves:
        if board[r][c] == "":
            square_labels[r][c].config(text="•", fg="blue")  # Empty square
        elif board[r][c] in (white_pieces.values() if piece in black_pieces.values() else black_pieces.values()):
            square_labels[r][c].config(bg="red")  # Enemy piece (capture)

    return moves

def find_king_position(is_white):
    king_symbol = white_pieces["King"] if is_white else black_pieces["King"]
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_symbol:
                return (r, c)
    return None

def is_square_attacked(row, col, is_white):
    opponent_pieces = black_pieces.values() if is_white else white_pieces.values()
    for r in range(8):
        for c in range(8):
            if board[r][c] in opponent_pieces:
                piece = board[r][c]
                moves = []
                if piece in (black_pieces["Pawn"], white_pieces["Pawn"]):
                    moves = get_moves_for_pawn(r, c, piece in white_pieces.values())
                elif piece in (black_pieces["Knight"], white_pieces["Knight"]):
                    moves = get_moves_for_knight(r, c)
                elif piece in (black_pieces["Rook"], white_pieces["Rook"]):
                    moves = get_moves_for_rook(r, c)
                elif piece in (black_pieces["Bishop"], white_pieces["Bishop"]):
                    moves = get_moves_for_bishop(r, c)
                elif piece in (black_pieces["Queen"], white_pieces["Queen"]):
                    moves = get_moves_for_queen(r, c)
                elif piece in (black_pieces["King"], white_pieces["King"]):
                    moves = get_moves_for_king(r, c)
                if (row, col) in moves:
                    return True
    return False

def is_king_in_check(is_white):
    king_pos = find_king_position(is_white)
    if not king_pos:
        return False  # King not found (should not happen in a valid game)
    return is_square_attacked(*king_pos, is_white)

def restrict_moves_to_king():
    global selected_piece, selected_pos

    reset_highlights()
    king_pos = find_king_position(turn == "white")
    if king_pos:
        row, col = king_pos
        selected_piece = board[row][col]
        selected_pos = (row, col)
        highlight_moves(row, col)
        

def is_checkmate(is_white):
    king_pos = find_king_position(is_white)
    if not king_pos:
        return False  # King not found (should not happen in a valid game)
    
    if not is_square_attacked(*king_pos, is_white):
        return False  # King is not in check
    
    # Check if the king has any valid moves to escape
    king_moves = get_moves_for_king(*king_pos)
    for r, c in king_moves:
        if not is_square_attacked(r, c, is_white):
            return False  # King can escape to a safe square

    # Check if any other piece can block the check or capture the attacker
    for r in range(8):
        for c in range(8):
            if board[r][c] in (white_pieces.values() if is_white else black_pieces.values()):
                piece = board[r][c]
                original_pos = (r, c)
                valid_moves = []

                if piece in (white_pieces["Pawn"], black_pieces["Pawn"]):
                    valid_moves = get_moves_for_pawn(r, c, piece in white_pieces.values())
                elif piece in (white_pieces["Knight"], black_pieces["Knight"]):
                    valid_moves = get_moves_for_knight(r, c)
                elif piece in (white_pieces["Rook"], black_pieces["Rook"]):
                    valid_moves = get_moves_for_rook(r, c)
                elif piece in (white_pieces["Bishop"], black_pieces["Bishop"]):
                    valid_moves = get_moves_for_bishop(r, c)
                elif piece in (white_pieces["Queen"], black_pieces["Queen"]):
                    valid_moves = get_moves_for_queen(r, c)

                for move in valid_moves:
                    old_piece = board[move[0]][move[1]]  # Backup the captured piece
                    board[move[0]][move[1]] = piece
                    board[r][c] = ""  # Temporarily move the piece

                    if not is_square_attacked(*king_pos, is_white):
                        board[r][c] = piece  # Undo the move
                        board[move[0]][move[1]] = old_piece
                        return False  # A move can save the king

                    board[r][c] = piece  # Undo the move
                    board[move[0]][move[1]] = old_piece

    return True  # No moves can save the king


def reset_highlights():
    for r in range(8):
        for c in range(8):
            if square_labels[r][c].cget("bg") != "blue":  # Keep blue cells for castled king
                bg_color = light_square if (r + c) % 2 == 0 else dark_square
                piece = board[r][c]
                color = "white" if piece in white_pieces.values() else "black"
                square_labels[r][c].config(bg=bg_color, text=piece, fg=color)
            
            
def select_piece(event, row, col):
    global selected_piece, selected_pos

    if selected_piece:
        # If a piece is already selected, try to move it or perform castling
        valid_moves = highlight_moves(*selected_pos)
        if (row, col) in valid_moves:
            move_piece(row, col)
        elif can_castle(selected_pos[0], selected_pos[1], turn == "white"):
            if col == 2 or col == 6:  # Check if the clicked square is for castling
                if col == 2:
                    perform_castling(row, col, turn == "white", "queenside")
                elif col == 6:
                    perform_castling(row, col, turn == "white", "kingside")
        else:
            reset_highlights()  # Invalid move, reset highlights
        selected_piece = None
        selected_pos = None  # Reset selection state
    elif (turn == "white" and board[row][col] in white_pieces.values()) or (
        turn == "black" and board[row][col] in black_pieces.values()
    ):
        # Select a new piece if it's the correct turn
        selected_piece = board[row][col]
        selected_pos = (row, col)
        reset_highlights()
        highlight_moves(row, col)
        show_castling_hint(row, col, turn == "white")  # Show castling hints

        
        
def promote_pawn(row, col, is_white):
    # Create a new top-level window for promotion choices
    promotion_window = tk.Toplevel(root)
    promotion_window.title("Pawn Promotion")
    promotion_window.geometry("200x200")
    
    # Function to handle promotion based on the button clicked
    def promote_to(piece_choice):
        nonlocal promotion_window

        # Map the promotion choice to the appropriate piece
        if piece_choice == 'Q':
            promoted_piece = white_pieces["Queen"] if is_white else black_pieces["Queen"]
        elif piece_choice == 'R':
            promoted_piece = white_pieces["Rook"] if is_white else black_pieces["Rook"]
        elif piece_choice == 'B':
            promoted_piece = white_pieces["Bishop"] if is_white else black_pieces["Bishop"]
        else:  # piece_choice == 'N'
            promoted_piece = white_pieces["Knight"] if is_white else black_pieces["Knight"]

        # Promote the pawn
        board[row][col] = promoted_piece
        update_board()  # Update the board visually
        promotion_window.destroy()  # Close the promotion window
    
    # Create the promotion buttons
    button_texts = {"Q": "Queen", "R": "Rook", "B": "Bishop", "N": "Knight"}
    for piece, text in button_texts.items():
        button = tk.Button(promotion_window, text=f"{text}", command=lambda p=piece: promote_to(p))
        button.pack(fill=tk.X, padx=10, pady=5)


def can_castle(row, col, is_white):
    # Check if the piece selected is a King and is in the right position for castling
    if board[row][col] != (white_pieces["King"] if is_white else black_pieces["King"]):
        return False

    # Check if the king has already moved
    if (is_white and turn != "white") or (not is_white and turn != "black"):
        return False

    # Check if the king is in check
    if is_king_in_check(is_white):
        return False

    # Check if castling is possible: need to check the rook's conditions as well
    rook_col = 0 if col == 4 else 7
    rook = board[row][rook_col]
    if rook != (white_pieces["Rook"] if is_white else black_pieces["Rook"]):
        return False

    # Ensure no pieces are between the king and rook, and the squares the king moves across are empty
    step = 1 if col == 4 else -1
    for c in range(col + step, rook_col, step):
        if board[row][c] != "":
            return False

    # Ensure the squares the king moves across are not under attack
    for c in range(col + step, rook_col, step):
        if is_square_attacked(row, c, is_white):
            return False

    return True

def show_castling_hint(row, col, is_white):
    """Highlight the possible squares for castling if available"""
    if can_castle(row, col, is_white):
        # Clear previous hints first
        reset_highlights()

        # Display castling path (arrows or symbols) to indicate the king's movement
        if col == 4:  # King's initial position
            if is_white:
                # Queenside castling (King goes to c1 and rook moves to d1)
                square_labels[row][3].config(bg="yellow", text="←", font=("Arial", 16, "bold"))
                # Kingside castling (King goes to g1 and rook moves to f1)
                square_labels[row][5].config(bg="yellow", text="→", font=("Arial", 16, "bold"))
            else:
                # Queenside castling (King goes to c8 and rook moves to d8)
                square_labels[row][3].config(bg="yellow", text="←", font=("Arial", 16, "bold"))
                # Kingside castling (King goes to g8 and rook moves to f8)
                square_labels[row][5].config(bg="yellow", text="→", font=("Arial", 16, "bold"))



                

def perform_castling(row, col, is_white, side):
    global white_king_moved, white_rook_king_side_moved, white_rook_queen_side_moved
    global black_king_moved, black_rook_king_side_moved, black_rook_queen_side_moved
    
    # Ensure the king hasn't moved already
    if is_white:
        white_king_moved = True
    else:
        black_king_moved = True

    # Mark rook as moved based on side (kingside or queenside)
    if is_white:
        if side == "kingside":
            white_rook_king_side_moved = True
        elif side == "queenside":
            white_rook_queen_side_moved = True
    else:
        if side == "kingside":
            black_rook_king_side_moved = True
        elif side == "queenside":
            black_rook_queen_side_moved = True
    
    # Move the King and Rook based on the side
    if side == "kingside":
        if is_white:
            board[7][6] = white_pieces["King"]  # Move the King
            board[7][5] = white_pieces["Rook"]  # Move the Rook
        else:
            board[0][6] = black_pieces["King"]  # Move the King
            board[0][5] = black_pieces["Rook"]  # Move the Rook
    elif side == "queenside":
        if is_white:
            board[7][2] = white_pieces["King"]  # Move the King
            board[7][3] = white_pieces["Rook"]  # Move the Rook
        else:
            board[0][2] = black_pieces["King"]  # Move the King
            board[0][3] = black_pieces["Rook"]  # Move the Rook
    
    # Clear the original squares
    board[7][4] = "" if is_white else ""  # King's original position
    board[0][4] = "" if not is_white else ""  # King's original position
    
    update_board()  # Update the board visually after castling

 # Change turn after castling


def move_piece(row, col):
    global selected_piece, selected_pos, last_move

    if selected_piece is None or selected_pos is None:
        return  # Ensure selection state is valid

    old_row, old_col = selected_pos
    captured_piece = board[row][col]  # Check if a piece is being captured

    # Handle en passant
    if selected_piece == white_pieces["Pawn"] or selected_piece == black_pieces["Pawn"]:
        # White en passant
        if selected_piece == white_pieces["Pawn"] and (row, col) == (old_row - 1, old_col + 1) and board[row][col] == "" and last_move == ((row + 1, col), (row - 1, col), black_pieces["Pawn"]):
            captured_piece = board[row + 1][col]  # Capture the black pawn
            board[row + 1][col] = ""  # Remove the captured pawn
        elif selected_piece == white_pieces["Pawn"] and (row, col) == (old_row - 1, old_col - 1) and board[row][col] == "" and last_move == ((row + 1, col), (row - 1, col), black_pieces["Pawn"]):
            captured_piece = board[row + 1][col]
            board[row + 1][col] = ""

        # Black en passant
        elif selected_piece == black_pieces["Pawn"] and (row, col) == (old_row + 1, old_col + 1) and board[row][col] == "" and last_move == ((row - 1, col), (row + 1, col), white_pieces["Pawn"]):
            captured_piece = board[row - 1][col]  # Capture the white pawn
            board[row - 1][col] = ""  # Remove the captured pawn
        elif selected_piece == black_pieces["Pawn"] and (row, col) == (old_row + 1, old_col - 1) and board[row][col] == "" and last_move == ((row - 1, col), (row + 1, col), white_pieces["Pawn"]):
            captured_piece = board[row - 1][col]
            board[row - 1][col] = ""

    board[row][col] = selected_piece
    board[old_row][old_col] = ""  # Clear the old position

    # Check for pawn promotion
    if selected_piece == white_pieces["Pawn"] and row == 0:
        promote_pawn(row, col, is_white=True)
    elif selected_piece == black_pieces["Pawn"] and row == 7:
        promote_pawn(row, col, is_white=False)

    # Update the board visually
    update_board()

    # Check if a king has been captured
    if captured_piece == white_pieces["King"]:
        messagebox.showinfo("Game Over!", "Black wins! White's King has been captured.")
        root.quit()
    elif captured_piece == black_pieces["King"]:
        messagebox.showinfo("Game Over!", "White wins! Black's King has been captured.")
        root.quit()

    # Ensure the move doesn't leave the current player's king in check
    if is_king_in_check(turn == "white" if turn == "black" else "black"):
        messagebox.showwarning("Invalid Move!", f"{turn.capitalize()} cannot leave their King in check!")
        # Undo the move
        board[old_row][old_col] = selected_piece
        board[row][col] = captured_piece
        update_board()
        reset_highlights()
        return

    # Track the last move
    last_move = ((old_row, old_col), (row, col), selected_piece)

    # Reset selection and toggle the turn
    selected_piece = None
    selected_pos = None
    toggle_turn()


def reset_game():
    global board, last_move, en_passant_pawns, turn
    last_move = None
    en_passant_pawns = []  # Clear en passant list
    turn = "white"  # Track whose turn it is# turn = "white" # Ensure white always starts after reset

    # Reset the board to the initial setup
    board = [
        [black_pieces["Rook"], black_pieces["Knight"], black_pieces["Bishop"], black_pieces["Queen"],
         black_pieces["King"], black_pieces["Bishop"], black_pieces["Knight"], black_pieces["Rook"]],
        [black_pieces["Pawn"]] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [white_pieces["Pawn"]] * 8,
        [white_pieces["Rook"], white_pieces["Knight"], white_pieces["Bishop"], white_pieces["Queen"],
         white_pieces["King"], white_pieces["Bishop"], white_pieces["Knight"], white_pieces["Rook"]],
    ]

    reset_highlights()  # Reset all visual customizations on the board
    update_board()  # Refresh the board pieces visually  # Function to update the visual display of the board (you'll need to define this function based on your setup)

# Key binding to reset the game when 'r' is pressed
root.bind("<r>", lambda event: reset_game())

def update_board():
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            color = "white" if piece in white_pieces.values() else "black"
            square_labels[r][c].config(text=piece, fg=color)
def toggle_turn():
    global turn
    turn = "black" if turn == "white" else "white"

    if is_king_in_check(turn == "white"):
        if is_checkmate(turn == "white"):
            messagebox.showinfo("Checkmate!", f"Checkmate! {turn.capitalize()} loses!")
            root.quit()  # End the game
        else:
            messagebox.showwarning("Check!", f"{turn.capitalize()} King is in check!")
            restrict_moves_to_king()
        return
    # Normal turn transition
    if not is_checkmate(turn == "white"):
        reset_highlights()


square_labels = [[None for _ in range(8)] for _ in range(8)]
for row in range(8):
    for col in range(8):
        bg_color = light_square if (row + col) % 2 == 0 else dark_square
        piece_color = "white" if board[row][col] in white_pieces.values() else "black"
        label = tk.Label(
            board_frame, text=board[row][col], font=("Arial", 32, "bold"),
            bg=bg_color, fg=piece_color, width=2, height=1
        )
        label.grid(row=row, column=col)
        label.bind("<Button-1>", lambda e, r=row, c=col: select_piece(e, r, c))
        square_labels[row][col] = label

root.mainloop()
