import sys
sys.path.insert(0, '../')
from GameBoard import GameBoard
import tkinter as tk
from OtherStuff import WHITE, BLACK, BOARD_SIZE, WHITE_KING, BLACK_KING, EMPTY

class CheckerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Checkers")
        self.square_size = 60
        self.board_size_px = BOARD_SIZE * self.square_size
        self.root.geometry(f"1000x{self.board_size_px + 180}")
        self.root.minsize(900, self.board_size_px + 150)

        self.game_board = GameBoard()
        self.status_var = tk.StringVar(value="White to move")
        self.current_player = WHITE
        self.selected_pos = None
        self.valid_moves = []
        self.game_over = False
        self.must_continue_jumping = False

        self.create_ui_layout()
        self.turn_label.config(text="👤 WHITE'S TURN")
        self.draw_board()
        self.root.mainloop()

    def create_ui_layout(self):
        header_frame = tk.Frame(self.root, bg="#f8f8f8")
        header_frame.pack(fill=tk.X, pady=(10,5))
        tk.Label(header_frame, text="🎯 Checkers", font=("Arial", 18, "bold"), bg="#f8f8f8").pack(side=tk.LEFT, padx=(15,0))
        self.turn_label = tk.Label(header_frame, text="👤 WHITE'S TURN", font=("Arial", 16, "bold"), bg="#f8f8f8")
        self.turn_label.pack(side=tk.RIGHT, padx=15)

        tk.Button(self.root, text="🔄 New Game", command=self.new_game, font=("Arial", 12, "bold"), 
                 bg="#4CAF50", fg="white", relief=tk.RAISED, bd=2, padx=15).pack(pady=(5,15))

        self.canvas = tk.Canvas(self.root, width=self.board_size_px, height=self.board_size_px, 
                               bg="#ffdbac", relief=tk.RAISED, bd=3)
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.status_label = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, 
                                   font=("Arial", 12), anchor=tk.W, padx=10, pady=5, bg="#e0e0e0")
        self.status_label.pack(fill=tk.X, padx=15, pady=(5,15))

    def new_game(self):
        self.game_board = GameBoard()
        self.current_player = WHITE
        self.selected_pos = None
        self.valid_moves = []
        self.game_over = False
        self.must_continue_jumping = False
        self.status_var.set("White to move")
        self.turn_label.config(text="👤 WHITE'S TURN")
        self.draw_board()

    def get_valid_moves(self, row, col):
        """🎯 CRITICAL FIX: ALL MOVES SHOWN (jumps + regular)"""
        piece = self.game_board.board[row][col]
        if piece not in [self.current_player, self.current_player.lower()]:
            return []
        
        moves = []
        
        # JUMPS (2 squares diagonal)
        for dr, dc in [(-2,-2), (-2,2), (2,-2), (2,2)]:
            tr, tc = row + dr, col + dc
            if 0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE:
                if self.game_board.is_valid_move(row, col, tr, tc, self.current_player):
                    moves.append((tr, tc))
        
        # REGULAR MOVES (1 square diagonal)
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            tr, tc = row + dr, col + dc
            if 0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE:
                if self.game_board.is_valid_move(row, col, tr, tc, self.current_player):
                    moves.append((tr, tc))
        
        return moves  # ALL MOVES - NO FILTERING

    def draw_board(self):
        self.canvas.delete("all")
        
        # Board
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1 = c * self.square_size
                y1 = r * self.square_size
                color = "saddlebrown" if (r+c) % 2 else "wheat"
                self.canvas.create_rectangle(x1, y1, x1+self.square_size, y1+self.square_size,
                                           fill=color, outline="brown", width=1)

        # MOVES: RED=jumps, GREEN=regular
        if self.selected_pos:
            fr, fc = self.selected_pos
            for tr, tc in self.valid_moves:
                xc = tc * self.square_size + self.square_size//2
                yc = tr * self.square_size + self.square_size//2
                is_jump = abs(tr - fr) == 2
                
                if is_jump:
                    self.canvas.create_oval(xc-22, yc-22, xc+22, yc+22, fill="#ff4444", outline="#cc0000", width=3)
                else:
                    self.canvas.create_oval(xc-18, yc-18, xc+18, yc+18, fill="#90EE90", outline="#228B22", width=2)

        # Selected piece
        if self.selected_pos:
            sr, sc = self.selected_pos
            xc = sc * self.square_size + self.square_size//2
            yc = sr * self.square_size + self.square_size//2
            self.canvas.create_oval(xc-28, yc-28, xc+28, yc+28, outline="#ff0000", width=4)

        self.draw_pieces()

    def draw_pieces(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.game_board.board[r][c]
                if piece != EMPTY:
                    xc = c * self.square_size + self.square_size//2
                    yc = r * self.square_size + self.square_size//2
                    
                    if piece in [WHITE, WHITE_KING]:
                        self.canvas.create_oval(xc-24, yc-24, xc+24, yc+24, fill="white", outline="#d4af37", width=3)
                    elif piece in [BLACK, BLACK_KING]:
                        self.canvas.create_oval(xc-24, yc-24, xc+24, yc+24, fill="black", outline="#c0c0c0", width=3)
                    
                    if piece == WHITE_KING:
                        self.canvas.create_polygon(xc-12, yc-26, xc+12, yc-26, xc, yc-8, fill="gold")
                    elif piece == BLACK_KING:
                        self.canvas.create_polygon(xc-12, yc-26, xc+12, yc-26, xc, yc-8, fill="silver")

    def check_game_over(self):
        white_count = sum(1 for row in self.game_board.board for cell in row if cell.upper() == WHITE)
        black_count = sum(1 for row in self.game_board.board for cell in row if cell.upper() == BLACK)
        
        if white_count == 0:
            self.game_over = True
            self.status_var.set("🏆 BLACK WINS!")
            self.turn_label.config(text="GAME OVER - BLACK WINS!")
            return True
        elif black_count == 0:
            self.game_over = True
            self.status_var.set("🏆 WHITE WINS!")
            self.turn_label.config(text="GAME OVER - WHITE WINS!")
            return True
        elif not self.game_board.has_any_legal_move(self.current_player):
            winner = BLACK if self.current_player == WHITE else WHITE
            self.game_over = True
            self.status_var.set(f"🏆 {winner.upper()} WINS!")
            self.turn_label.config(text=f"GAME OVER - {winner.upper()} WINS!")
            return True
        return False

    def on_canvas_click(self, event):
        if self.game_over: return

        col = event.x // self.square_size
        row = event.y // self.square_size
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE): return

        piece = self.game_board.board[row][col]

        # Multi-jump mode
        if self.must_continue_jumping and self.selected_pos:
            fr, fc = self.selected_pos
            if (row, col) in self.valid_moves:
                self.game_board.make_move(fr, fc, row, col, self.current_player)
                
                # More jumps?
                jumps = [(r,c) for r,c in self.get_valid_moves(row, col) if abs(r-row) == 2]
                if jumps:
                    self.selected_pos = (row, col)
                    self.valid_moves = jumps
                    self.must_continue_jumping = True
                    self.status_var.set(f"🔥 CONTINUE JUMP! ({len(jumps)} left)")
                else:
                    self.status_var.set("✅ Jumps done!")
                    self.selected_pos = None
                    self.valid_moves = []
                    self.must_continue_jumping = False
                    if not self.check_game_over():
                        self.switch_turn()
                self.draw_board()
            return

        # Select piece
        if piece in [self.current_player, self.current_player.lower()]:
            self.selected_pos = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            jumps = sum(1 for r,c in self.valid_moves if abs(r-row) == 2)
            total = len(self.valid_moves)
            self.status_var.set(f"🔴{jumps} jumps + 🟢{total-jumps} moves")
            self.draw_board()
            return

        # Move
        elif self.selected_pos:
            fr, fc = self.selected_pos
            if (row, col) in self.valid_moves:
                result = self.game_board.make_move(fr, fc, row, col, self.current_player)
                is_jump = abs(row - fr) == 2
                
                if is_jump:
                    jumps = [(r,c) for r,c in self.get_valid_moves(row, col) if abs(r-row) == 2]
                    if jumps:
                        self.selected_pos = (row, col)
                        self.valid_moves = jumps
                        self.must_continue_jumping = True
                        self.status_var.set(f"🔥 MUST JUMP! ({len(jumps)} left)")
                        self.draw_board()
                        return
                
                self.status_var.set("Move complete!")
                self.selected_pos = None
                self.valid_moves = []
                self.must_continue_jumping = False
                if not self.check_game_over():
                    self.switch_turn()
                self.draw_board()
            else:
                self.status_var.set("❌ Click valid square!")

    def switch_turn(self):
        self.current_player = BLACK if self.current_player == WHITE else WHITE
        self.turn_label.config(text=f"👤 {self.current_player}'s TURN")

if __name__ == "__main__":
    app = CheckerGUI()
