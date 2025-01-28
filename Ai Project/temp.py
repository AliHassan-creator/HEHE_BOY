import tkinter as tk
import random


root = tk.Tk()
root.title("Chess Board")
last_move = None
en_passant_pawns = []



white_pieces = {
    "Pawn": "\u2659",
    "Rook": "\u2656",
    "Knight": "\u2658",
    "Bishop": "\u2657",
    "Queen": "\u2655",
    "King": "\u2654",
}
root.geometry("640x640")
root.configure(bg="grey")


black_pieces = {
    "Pawn": "\u265F",
    "Rook": "\u265C",
    "Knight": "\u265E",
    "Bishop": "\u265D",
    "Queen": "\u265B",
    "King": "\u265A",
}


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

light_square = "#87CEEB"  
dark_square = "#DAA520"   

"""light_square = "#EEE8AA"  """
"""dark_square = "#8B4513"   """



board_frame = tk.Frame(root)
board_frame.pack(expand=True)


selected_piece = None
selected_pos = None


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

        # En passant condition
        if is_white and row == 4:  # White pawn on rank 5
            if col > 0 and board[row][col - 1] == black_pieces["Pawn"]:
                # En passant check for left pawn
                if last_move and last_move == (row - 2, col - 1, row - 1, col - 1):
                    moves.append((row + direction, col - 1))  # En passant capture
            if col < 7 and board[row][col + 1] == black_pieces["Pawn"]:
                # En passant check for right pawn
                if last_move and last_move == (row - 2, col + 1, row - 1, col + 1):
                    moves.append((row + direction, col + 1))  # En passant capture
        elif not is_white and row == 3:  # Black pawn on rank 4
            if col > 0 and board[row][col - 1] == white_pieces["Pawn"]:
                # En passant check for left pawn
                if last_move and last_move == (row + 2, col - 1, row + 1, col - 1):
                    moves.append((row + direction, col - 1))  # En passant capture
            if col < 7 and board[row][col + 1] == white_pieces["Pawn"]:
                # En passant check for right pawn
                if last_move and last_move == (row + 2, col + 1, row + 1, col + 1):
                    moves.append((row + direction, col + 1))  # En passant capture

    return moves

def set_last_move(start_row, start_col, end_row, end_col):
    global last_move, en_passant_pawns
    last_move = (start_row, start_col, end_row, end_col)

    # Check for en passant move (pawn moving two squares forward)
    if abs(start_row - end_row) == 2 and board[start_row][start_col] in (white_pieces["Pawn"], black_pieces["Pawn"]):
        en_passant_pawns.append((end_row, end_col))  # Mark pawn as eligible for en passant
    else:
        en_passant_pawns = [pawn for pawn in en_passant_pawns if pawn != (end_row, end_col)]  # Remove pawn if no longer eligible



def get_moves_for_knight(row, col):
    moves = []
    knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in (white_pieces.values() if board[row][col] in white_pieces.values() else black_pieces.values()):
            moves.append((r, c))
    return moves


def get_moves_for_rook(row, col):
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return get_sliding_piece_moves(row, col, directions)


def get_moves_for_bishop(row, col):
    
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_sliding_piece_moves(row, col, directions)


def get_moves_for_queen(row, col):
    return get_moves_for_rook(row, col) + get_moves_for_bishop(row, col)


def get_moves_for_king(row, col):
    moves = []
    king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in (white_pieces.values() if board[row][col] in white_pieces.values() else black_pieces.values()):
            moves.append((r, c))
    
    # Add castling moves, fix the logic to prevent unnecessary restrictions
    if board[row][col] == white_pieces["King"]:
        # Check kingside castling
        if row == 7 and col == 4:  # White's King starting position
            if (board[7][7] == white_pieces["Rook"] and  # White's kingside rook is present
                board[7][5] == "" and board[7][6] == "" and  # The squares between are empty
                not is_square_threatened(7, 4, is_white=True) and  # King is not in check
                not is_square_threatened(7, 5, is_white=True) and  # King is not in check during castling
                not is_square_threatened(7, 6, is_white=True)):  # King is not in check during castling
                moves.append((7, 6))  # Kingside castling move
                
        # Check queenside castling
        if row == 7 and col == 4:  # White's King starting position
            if (board[7][0] == white_pieces["Rook"] and  # White's queenside rook is present
                board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and  # The squares between are empty
                not is_square_threatened(7, 4, is_white=True) and  # King is not in check
                not is_square_threatened(7, 3, is_white=True) and  # King is not in check during castling
                not is_square_threatened(7, 2, is_white=True)):  # King is not in check during castling
                moves.append((7, 2))  # Queenside castling move

    elif board[row][col] == black_pieces["King"]:
        # Check kingside castling
        if row == 0 and col == 4:  # Black's King starting position
            if (board[0][7] == black_pieces["Rook"] and  # Black's kingside rook is present
                board[0][5] == "" and board[0][6] == "" and  # The squares between are empty
                not is_square_threatened(0, 4, is_white=False) and  # King is not in check
                not is_square_threatened(0, 5, is_white=False) and  # King is not in check during castling
                not is_square_threatened(0, 6, is_white=False)):  # King is not in check during castling
                moves.append((0, 6))  # Kingside castling move

        # Check queenside castling
        if row == 0 and col == 4:  # Black's King starting position
            if (board[0][0] == black_pieces["Rook"] and  # Black's queenside rook is present
                board[0][1] == "" and board[0][2] == "" and board[0][3] == "" and  # The squares between are empty
                not is_square_threatened(0, 4, is_white=False) and  # King is not in check
                not is_square_threatened(0, 3, is_white=False) and  # King is not in check during castling
                not is_square_threatened(0, 2, is_white=False)):  # King is not in check during castling
                moves.append((0, 2))  # Queenside castling move

    return moves




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

def show_check_popup(king_color):
    check_message = f"{king_color} King is in opponents checkmate position!"
    popup = tk.Toplevel(root)
    popup.title("Check!")
    label = tk.Label(popup, text=check_message, font=("Arial", 14))
    label.pack(padx=20, pady=20)
    button = tk.Button(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)


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

    # Highlight possible moves
    for r, c in moves:
        if board[r][c] == "":
            square_labels[r][c].config(text="•", fg="blue")  # Empty square
        elif board[r][c] in (white_pieces.values() if piece in black_pieces.values() else black_pieces.values()):
            square_labels[r][c].config(bg="red")  # Enemy piece (capture)

    # Highlight en passant pawns
    if (row, col) in en_passant_pawns:
        square_labels[row][col].config(bg="yellow")  # Highlight en passant pawns

    return moves

def is_king_in_check(is_white):
    """Check if the King of the given color is in check."""
    king_piece = white_pieces["King"] if is_white else black_pieces["King"]

    # Locate the King's position
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_piece:
                if is_square_threatened(r, c, is_white):
                    
                    square_labels[r][c].config(bg="blue")
                    king_color = "White" if is_white else "Black"
                    show_check_popup(king_color)
                    return True
    return False

def is_black_king_in_check():
    """Check if the black king is in check."""
    black_king_position = None

    # Locate the black king's position
    for r in range(8):
        for c in range(8):
            if board[r][c] == black_pieces["King"]:
                black_king_position = (r, c)
                break
        if black_king_position:
            break

    if not black_king_position:
        return False  # Black king is not on the board (unlikely scenario)

    black_king_row, black_king_col = black_king_position

    # Check if any white piece is threatening the black king
    for r in range(8):
        for c in range(8):
            if board[r][c] in white_pieces.values():
                moves = highlight_moves(r, c)
                if (black_king_row, black_king_col) in moves:
                    # Highlight the king's square in blue when in check
                    square_labels[black_king_row][black_king_col].config(bg="blue")
                    show_check_popup("Black")
                    return True

    return False

def is_white_king_in_check():
    """Check if the white king is in check."""
    white_king_position = None

    # Locate the white king's position
    for r in range(8):
        for c in range(8):
            if board[r][c] == white_pieces["King"]:
                white_king_position = (r, c)
                break
        if white_king_position:
            break

    if not white_king_position:
        return False  # White king is not on the board (unlikely scenario)

    white_king_row, white_king_col = white_king_position

    # Check if any black piece is threatening the white king
    for r in range(8):
        for c in range(8):
            if board[r][c] in black_pieces.values():
                moves = highlight_moves(r, c)
                if (white_king_row, white_king_col) in moves:
                    # Highlight the king's square in blue when in check
                    square_labels[white_king_row][white_king_col].config(bg="blue")
                    show_check_popup("White")
                    return True

    return False


def perform_black_move():
    """Perform the black player's move, prioritizing valuable captures and strategic positioning."""
    all_moves = []

    # Collect all possible moves for black pieces
    for row in range(8):
        for col in range(8):
            if board[row][col] in black_pieces.values():
                moves = highlight_moves(row, col)
                for move in moves:
                    all_moves.append((row, col, move))

    if not all_moves:
        return  # No moves available (game over or stalemate)

    # Evaluate each move with a scoring system
    def evaluate_move(old_row, old_col, new_row, new_col):
        score = 0
        target_piece = board[new_row][new_col]

        # Capture value (prioritize high-value captures)
        piece_values = {
            white_pieces["King"]: 1000,  # King is the highest priority
            white_pieces["Queen"]: 9,
            white_pieces["Rook"]: 5,
            white_pieces["Bishop"]: 3,
            white_pieces["Knight"]: 3,
            white_pieces["Pawn"]: 1,
        }
        score += piece_values.get(target_piece, 0)

        # Positional advantage: Prefer moves toward the center
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if (new_row, new_col) in center_squares:
            score += 2  # Bonus for controlling the center

        # Safety check: Avoid moving into positions where the piece can be captured
        if is_square_threatened(new_row, new_col, is_white=False):
            score -= 5  # Penalize unsafe moves

        # Threat potential: Reward moves that threaten enemy pieces
        enemy_threatened = any(
            board[r][c] in white_pieces.values()
            for r, c in highlight_moves(new_row, new_col)
        )
        if enemy_threatened:
            score += 3

        return score

    # Sort all moves based on the evaluation
    all_moves.sort(
        key=lambda move: evaluate_move(*move[0:2], *move[2]), reverse=True
    )

    best_move = all_moves[0]
    old_row, old_col, (new_row, new_col) = best_move
    board[new_row][new_col] = board[old_row][old_col]
    board[old_row][old_col] = ""
    update_board()


def promote_pawn(row, col, is_white):
    """Display a popup to promote a pawn when it reaches the last rank."""
    promotion_popup = tk.Toplevel(root)
    promotion_popup.title("Promote Pawn")
    promotion_popup.geometry("200x200")

    def select_promotion(piece_name):
        board[row][col] = white_pieces[piece_name] if is_white else black_pieces[piece_name]
        promotion_popup.destroy()
        update_board()

    promotion_pieces = ["Queen", "Rook", "Bishop", "Knight"]
    for piece in promotion_pieces:
        button = tk.Button(
            promotion_popup, text=piece, command=lambda p=piece: select_promotion(p)
        )
        button.pack(fill=tk.BOTH, expand=True)

def is_square_threatened(row, col, is_white):
    """Check if a square is threatened by the opponent."""
    enemy_pieces = white_pieces.values() if not is_white else black_pieces.values()
    for r in range(8):
        for c in range(8):
            if board[r][c] in enemy_pieces:
                # Generate legal moves for the enemy piece
                if board[r][c] in (white_pieces["Pawn"], black_pieces["Pawn"]):
                    moves = get_moves_for_pawn(r, c, board[r][c] in white_pieces.values())
                elif board[r][c] in (white_pieces["Knight"], black_pieces["Knight"]):
                    moves = get_moves_for_knight(r, c)
                elif board[r][c] in (white_pieces["Rook"], black_pieces["Rook"]):
                    moves = get_moves_for_rook(r, c)
                elif board[r][c] in (white_pieces["Bishop"], black_pieces["Bishop"]):
                    moves = get_moves_for_bishop(r, c)
                elif board[r][c] in (white_pieces["Queen"], black_pieces["Queen"]):
                    moves = get_moves_for_queen(r, c)
                elif board[r][c] in (white_pieces["King"], black_pieces["King"]):
                    moves = get_moves_for_king(r, c)
                else:
                    continue

                if (row, col) in moves:
                    return True
    return False


def reset_highlights():
    
    for r in range(8):
        for c in range(8):
            bg_color = light_square if (r + c) % 2 == 0 else dark_square
            square_labels[r][c].config(bg=bg_color, text=board[r][c], fg="black" if board[r][c] in black_pieces.values() else "white")


def select_piece(event, row, col):
    
    global selected_piece, selected_pos

    if selected_piece:
        move_piece(row, col)
    elif board[row][col] in white_pieces.values():
        selected_piece = board[row][col]
        selected_pos = (row, col)
        reset_highlights()
        highlight_moves(row, col)


def move_piece(row, col):
    global selected_piece, selected_pos, last_move, current_turn

    if (row, col) in highlight_moves(*selected_pos):
        old_row, old_col = selected_pos
        piece = board[old_row][old_col]
        
        # Castling logic
        if piece == white_pieces["King"] and old_row == 7 and old_col == 4:
            if col == 6:  # Kingside castling
                board[7][5] = white_pieces["Rook"]
                board[7][7] = ""
            elif col == 2:  # Queenside castling
                board[7][3] = white_pieces["Rook"]
                board[7][0] = ""
                
        elif piece == black_pieces["King"] and old_row == 0 and old_col == 4:
            if col == 6:  # Kingside castling
                board[0][5] = black_pieces["Rook"]
                board[0][7] = ""
            elif col == 2:  # Queenside castling
                board[0][3] = black_pieces["Rook"]
                board[0][0] = ""

        else:
            # Regular piece move
            board[row][col] = piece
            board[old_row][old_col] = ""

        # Set the last move
        set_last_move(old_row, old_col, row, col)

        # Check for en passant capture
        if (row, col) in get_moves_for_pawn(row, col, piece in white_pieces.values()):
            if piece == white_pieces["Pawn"] and old_row == 6 and row == 4:
                set_last_move(old_row, old_col, row, col)
            elif piece == black_pieces["Pawn"] and old_row == 1 and row == 3:
                set_last_move(old_row, old_col, row, col)

        # Check for pawn promotion
        if piece == white_pieces["Pawn"] and row == 0:
            promote_pawn(row, col, is_white=True)
        elif piece == black_pieces["Pawn"] and row == 7:
            promote_pawn(row, col, is_white=False)

        # Check if the black king is in check
        if is_black_king_in_check():
            print("Black King is in opponents checkmate position!")

        # Check if the white king is in check
        if is_white_king_in_check():
            print("White King is in opponents checkmate position!")

        # End White's turn and switch to Black's turn
        current_turn = False  # Now it's Black's turn (Black is not allowed to move)

        # Perform the black move (this can be handled by the AI or whatever logic you prefer)
        perform_black_move()

    selected_piece = None
    selected_pos = None
    reset_highlights()

def reset_game():
    global board, last_move, en_passant_pawns
    last_move = None
    en_passant_pawns = []  # Clear en passant list

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
    
    update_board()  # Function to update the visual display of the board (you'll need to define this function based on your setup)

# Key binding to reset the game when 'r' is pressed
root.bind("<r>", lambda event: reset_game())


def update_board():
    
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            color = "white" if piece in white_pieces.values() else "black"
            square_labels[r][c].config(text=piece, fg=color)



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
import tkinter as tk
import random


root = tk.Tk()
root.title("Chess Board")
last_move = None
en_passant_pawns = []  # Store the positions of pawns eligible for en passant



white_pieces = {
    "Pawn": "\u2659",
    "Rook": "\u2656",
    "Knight": "\u2658",
    "Bishop": "\u2657",
    "Queen": "\u2655",
    "King": "\u2654",
}
root.geometry("640x640")
root.configure(bg="grey")


black_pieces = {
    "Pawn": "\u265F",
    "Rook": "\u265C",
    "Knight": "\u265E",
    "Bishop": "\u265D",
    "Queen": "\u265B",
    "King": "\u265A",
}


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

light_square = "#87CEEB"  
dark_square = "#DAA520"   

"""light_square = "#EEE8AA"  """
"""dark_square = "#8B4513"   """



board_frame = tk.Frame(root)
board_frame.pack(expand=True)


selected_piece = None
selected_pos = None


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

        # En passant condition
        if is_white and row == 4:  # White pawn on rank 5
            if col > 0 and board[row][col - 1] == black_pieces["Pawn"]:
                # En passant check for left pawn
                if last_move and last_move == (row - 2, col - 1, row - 1, col - 1):
                    moves.append((row + direction, col - 1))  # En passant capture
            if col < 7 and board[row][col + 1] == black_pieces["Pawn"]:
                # En passant check for right pawn
                if last_move and last_move == (row - 2, col + 1, row - 1, col + 1):
                    moves.append((row + direction, col + 1))  # En passant capture
        elif not is_white and row == 3:  # Black pawn on rank 4
            if col > 0 and board[row][col - 1] == white_pieces["Pawn"]:
                # En passant check for left pawn
                if last_move and last_move == (row + 2, col - 1, row + 1, col - 1):
                    moves.append((row + direction, col - 1))  # En passant capture
            if col < 7 and board[row][col + 1] == white_pieces["Pawn"]:
                # En passant check for right pawn
                if last_move and last_move == (row + 2, col + 1, row + 1, col + 1):
                    moves.append((row + direction, col + 1))  # En passant capture

    return moves

def set_last_move(start_row, start_col, end_row, end_col):
    global last_move, en_passant_pawns
    last_move = (start_row, start_col, end_row, end_col)

    # Check for en passant move (pawn moving two squares forward)
    if abs(start_row - end_row) == 2 and board[start_row][start_col] in (white_pieces["Pawn"], black_pieces["Pawn"]):
        en_passant_pawns.append((end_row, end_col))  # Mark pawn as eligible for en passant
    else:
        en_passant_pawns = [pawn for pawn in en_passant_pawns if pawn != (end_row, end_col)]  # Remove pawn if no longer eligible



def get_moves_for_knight(row, col):
    moves = []
    knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in (white_pieces.values() if board[row][col] in white_pieces.values() else black_pieces.values()):
            moves.append((r, c))
    return moves


def get_moves_for_rook(row, col):
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return get_sliding_piece_moves(row, col, directions)


def get_moves_for_bishop(row, col):
    
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_sliding_piece_moves(row, col, directions)


def get_moves_for_queen(row, col):
    return get_moves_for_rook(row, col) + get_moves_for_bishop(row, col)


def get_moves_for_king(row, col):
    moves = []
    king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in (white_pieces.values() if board[row][col] in white_pieces.values() else black_pieces.values()):
            moves.append((r, c))
    
    # Add castling moves, fix the logic to prevent unnecessary restrictions
    if board[row][col] == white_pieces["King"]:
        # Check kingside castling
        if row == 7 and col == 4:  # White's King starting position
            if (board[7][7] == white_pieces["Rook"] and  # White's kingside rook is present
                board[7][5] == "" and board[7][6] == "" and  # The squares between are empty
                not is_square_threatened(7, 4, is_white=True) and  # King is not in check
                not is_square_threatened(7, 5, is_white=True) and  # King is not in check during castling
                not is_square_threatened(7, 6, is_white=True)):  # King is not in check during castling
                moves.append((7, 6))  # Kingside castling move
                
        # Check queenside castling
        if row == 7 and col == 4:  # White's King starting position
            if (board[7][0] == white_pieces["Rook"] and  # White's queenside rook is present
                board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and  # The squares between are empty
                not is_square_threatened(7, 4, is_white=True) and  # King is not in check
                not is_square_threatened(7, 3, is_white=True) and  # King is not in check during castling
                not is_square_threatened(7, 2, is_white=True)):  # King is not in check during castling
                moves.append((7, 2))  # Queenside castling move

    elif board[row][col] == black_pieces["King"]:
        # Check kingside castling
        if row == 0 and col == 4:  # Black's King starting position
            if (board[0][7] == black_pieces["Rook"] and  # Black's kingside rook is present
                board[0][5] == "" and board[0][6] == "" and  # The squares between are empty
                not is_square_threatened(0, 4, is_white=False) and  # King is not in check
                not is_square_threatened(0, 5, is_white=False) and  # King is not in check during castling
                not is_square_threatened(0, 6, is_white=False)):  # King is not in check during castling
                moves.append((0, 6))  # Kingside castling move

        # Check queenside castling
        if row == 0 and col == 4:  # Black's King starting position
            if (board[0][0] == black_pieces["Rook"] and  # Black's queenside rook is present
                board[0][1] == "" and board[0][2] == "" and board[0][3] == "" and  # The squares between are empty
                not is_square_threatened(0, 4, is_white=False) and  # King is not in check
                not is_square_threatened(0, 3, is_white=False) and  # King is not in check during castling
                not is_square_threatened(0, 2, is_white=False)):  # King is not in check during castling
                moves.append((0, 2))  # Queenside castling move

    return moves




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

def show_check_popup(king_color):
    check_message = f"{king_color} King is in opponents checkmate position!"
    popup = tk.Toplevel(root)
    popup.title("Check!")
    label = tk.Label(popup, text=check_message, font=("Arial", 14))
    label.pack(padx=20, pady=20)
    button = tk.Button(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)


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

    # Highlight possible moves
    for r, c in moves:
        if board[r][c] == "":
            square_labels[r][c].config(text="•", fg="blue")  # Empty square
        elif board[r][c] in (white_pieces.values() if piece in black_pieces.values() else black_pieces.values()):
            square_labels[r][c].config(bg="red")  # Enemy piece (capture)

    # Highlight en passant pawns
    if (row, col) in en_passant_pawns:
        square_labels[row][col].config(bg="yellow")  # Highlight en passant pawns

    return moves

def is_king_in_check(is_white):
    """Check if the King of the given color is in check."""
    king_piece = white_pieces["King"] if is_white else black_pieces["King"]

    # Locate the King's position
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_piece:
                if is_square_threatened(r, c, is_white):
                    # Highlight the King's square
                    square_labels[r][c].config(bg="blue")
                    king_color = "White" if is_white else "Black"
                    show_check_popup(king_color)
                    return True
    return False

def is_black_king_in_check():
    """Check if the black king is in check."""
    black_king_position = None

    # Locate the black king's position
    for r in range(8):
        for c in range(8):
            if board[r][c] == black_pieces["King"]:
                black_king_position = (r, c)
                break
        if black_king_position:
            break

    if not black_king_position:
        return False  # Black king is not on the board (unlikely scenario)

    black_king_row, black_king_col = black_king_position

    # Check if any white piece is threatening the black king
    for r in range(8):
        for c in range(8):
            if board[r][c] in white_pieces.values():
                moves = highlight_moves(r, c)
                if (black_king_row, black_king_col) in moves:
                    # Highlight the king's square in blue when in check
                    square_labels[black_king_row][black_king_col].config(bg="blue")
                    show_check_popup("Black")
                    return True

    return False

def is_white_king_in_check():
    """Check if the white king is in check."""
    white_king_position = None

    # Locate the white king's position
    for r in range(8):
        for c in range(8):
            if board[r][c] == white_pieces["King"]:
                white_king_position = (r, c)
                break
        if white_king_position:
            break

    if not white_king_position:
        return False  # White king is not on the board (unlikely scenario)

    white_king_row, white_king_col = white_king_position

    # Check if any black piece is threatening the white king
    for r in range(8):
        for c in range(8):
            if board[r][c] in black_pieces.values():
                moves = highlight_moves(r, c)
                if (white_king_row, white_king_col) in moves:
                    # Highlight the king's square in blue when in check
                    square_labels[white_king_row][white_king_col].config(bg="blue")
                    show_check_popup("White")
                    return True

    return False


def perform_black_move():
    """Perform the black player's move, prioritizing valuable captures and strategic positioning."""
    all_moves = []

    # Collect all possible moves for black pieces
    for row in range(8):
        for col in range(8):
            if board[row][col] in black_pieces.values():
                moves = highlight_moves(row, col)
                for move in moves:
                    all_moves.append((row, col, move))

    if not all_moves:
        return  # No moves available (game over or stalemate)

    # Evaluate each move with a scoring system
    def evaluate_move(old_row, old_col, new_row, new_col):
        score = 0
        target_piece = board[new_row][new_col]

        # Capture value (prioritize high-value captures)
        piece_values = {
            white_pieces["King"]: 1000,  # King is the highest priority
            white_pieces["Queen"]: 9,
            white_pieces["Rook"]: 5,
            white_pieces["Bishop"]: 3,
            white_pieces["Knight"]: 3,
            white_pieces["Pawn"]: 1,
        }
        score += piece_values.get(target_piece, 0)

        # Positional advantage: Prefer moves toward the center
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if (new_row, new_col) in center_squares:
            score += 2  # Bonus for controlling the center

        # Safety check: Avoid moving into positions where the piece can be captured
        if is_square_threatened(new_row, new_col, is_white=False):
            score -= 5  # Penalize unsafe moves

        # Threat potential: Reward moves that threaten enemy pieces
        enemy_threatened = any(
            board[r][c] in white_pieces.values()
            for r, c in highlight_moves(new_row, new_col)
        )
        if enemy_threatened:
            score += 3

        return score

    # Sort all moves based on the evaluation
    all_moves.sort(
        key=lambda move: evaluate_move(*move[0:2], *move[2]), reverse=True
    )

    best_move = all_moves[0]
    old_row, old_col, (new_row, new_col) = best_move
    board[new_row][new_col] = board[old_row][old_col]
    board[old_row][old_col] = ""
    update_board()


def promote_pawn(row, col, is_white):
    """Display a popup to promote a pawn when it reaches the last rank."""
    promotion_popup = tk.Toplevel(root)
    promotion_popup.title("Promote Pawn")
    promotion_popup.geometry("200x200")

    def select_promotion(piece_name):
        board[row][col] = white_pieces[piece_name] if is_white else black_pieces[piece_name]
        promotion_popup.destroy()
        update_board()

    promotion_pieces = ["Queen", "Rook", "Bishop", "Knight"]
    for piece in promotion_pieces:
        button = tk.Button(
            promotion_popup, text=piece, command=lambda p=piece: select_promotion(p)
        )
        button.pack(fill=tk.BOTH, expand=True)

def is_square_threatened(row, col, is_white):
    """Check if a square is threatened by the opponent."""
    enemy_pieces = white_pieces.values() if not is_white else black_pieces.values()
    for r in range(8):
        for c in range(8):
            if board[r][c] in enemy_pieces:
                # Generate legal moves for the enemy piece
                if board[r][c] in (white_pieces["Pawn"], black_pieces["Pawn"]):
                    moves = get_moves_for_pawn(r, c, board[r][c] in white_pieces.values())
                elif board[r][c] in (white_pieces["Knight"], black_pieces["Knight"]):
                    moves = get_moves_for_knight(r, c)
                elif board[r][c] in (white_pieces["Rook"], black_pieces["Rook"]):
                    moves = get_moves_for_rook(r, c)
                elif board[r][c] in (white_pieces["Bishop"], black_pieces["Bishop"]):
                    moves = get_moves_for_bishop(r, c)
                elif board[r][c] in (white_pieces["Queen"], black_pieces["Queen"]):
                    moves = get_moves_for_queen(r, c)
                elif board[r][c] in (white_pieces["King"], black_pieces["King"]):
                    moves = get_moves_for_king(r, c)
                else:
                    continue

                if (row, col) in moves:
                    return True
    return False


def reset_highlights():
    
    for r in range(8):
        for c in range(8):
            bg_color = light_square if (r + c) % 2 == 0 else dark_square
            square_labels[r][c].config(bg=bg_color, text=board[r][c], fg="black" if board[r][c] in black_pieces.values() else "white")


def select_piece(event, row, col):
    
    global selected_piece, selected_pos

    if selected_piece:
        move_piece(row, col)
    elif board[row][col] in white_pieces.values():
        selected_piece = board[row][col]
        selected_pos = (row, col)
        reset_highlights()
        highlight_moves(row, col)


def move_piece(row, col):
    global selected_piece, selected_pos, last_move, current_turn

    if (row, col) in highlight_moves(*selected_pos):
        old_row, old_col = selected_pos
        piece = board[old_row][old_col]
        
        # Castling logic
        if piece == white_pieces["King"] and old_row == 7 and old_col == 4:
            if col == 6:  # Kingside castling
                board[7][5] = white_pieces["Rook"]
                board[7][7] = ""
            elif col == 2:  # Queenside castling
                board[7][3] = white_pieces["Rook"]
                board[7][0] = ""
                
        elif piece == black_pieces["King"] and old_row == 0 and old_col == 4:
            if col == 6:  # Kingside castling
                board[0][5] = black_pieces["Rook"]
                board[0][7] = ""
            elif col == 2:  # Queenside castling
                board[0][3] = black_pieces["Rook"]
                board[0][0] = ""

        else:
            # Regular piece move
            board[row][col] = piece
            board[old_row][old_col] = ""

        # Set the last move
        set_last_move(old_row, old_col, row, col)

        # Check for en passant capture
        if (row, col) in get_moves_for_pawn(row, col, piece in white_pieces.values()):
            if piece == white_pieces["Pawn"] and old_row == 6 and row == 4:
                set_last_move(old_row, old_col, row, col)
            elif piece == black_pieces["Pawn"] and old_row == 1 and row == 3:
                set_last_move(old_row, old_col, row, col)

        # Check for pawn promotion
        if piece == white_pieces["Pawn"] and row == 0:
            promote_pawn(row, col, is_white=True)
        elif piece == black_pieces["Pawn"] and row == 7:
            promote_pawn(row, col, is_white=False)

        # Check if the black king is in check
        if is_black_king_in_check():
            print("Black King is in opponents checkmate position!")

        # Check if the white king is in check
        if is_white_king_in_check():
            print("White King is in opponents checkmate position!")

        # End White's turn and switch to Black's turn
        current_turn = False  # Now it's Black's turn (Black is not allowed to move)

        # Perform the black move (this can be handled by the AI or whatever logic you prefer)
        perform_black_move()

    selected_piece = None
    selected_pos = None
    reset_highlights()

def reset_game():
    global board, last_move, en_passant_pawns
    last_move = None
    en_passant_pawns = []  # Clear en passant list

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
    
    update_board()  # Function to update the visual display of the board (you'll need to define this function based on your setup)

# Key binding to reset the game when 'r' is pressed
root.bind("<r>", lambda event: reset_game())


def update_board():
    
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            color = "white" if piece in white_pieces.values() else "black"
            square_labels[r][c].config(text=piece, fg=color)



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
