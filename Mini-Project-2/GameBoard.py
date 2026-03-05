
from constants import (BOARD_SIZE, WHITE, BLACK, WHITE_KING, BLACK_KING, EMPTY,
                       BLACK_ROWS, WHITE_ROWS, SIMPLE_MOVE, JUMP_MOVE, JUMP_DIRECTIONS)

class GameBoard:
    def __init__(self):
        self.board = []  # creating the board
        for row_number in range(BOARD_SIZE):
            one_row = []
            for col_number in range(BOARD_SIZE):
                one_row.append(EMPTY)  # creating a row that will be then integrated into the board
            
            self.board.append(one_row)

        self.setup_initial_board()


    def setup_initial_board(self):
        """Set up the initial checker pieces on the board."""
        # BLACK pieces - top 3 rows
        for row in BLACK_ROWS:
            for col in range(BOARD_SIZE):
                # Checkerboard pattern: odd columns for rows 0,2; even columns for row 1
                if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                    self.board[row][col] = BLACK

        # WHITE pieces - bottom 3 rows
        for row in WHITE_ROWS:
            for col in range(BOARD_SIZE):
                # Checkerboard pattern: even columns for rows 5,7; odd columns for row 6
                if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                    self.board[row][col] = WHITE

    def display_board(self):
        """Display the current state of the board with coordinates."""
        print("   ", end="")
        for col in range(BOARD_SIZE):
            print(f" {col}", end="")
        print()
        
        print("  +" + "-" * (BOARD_SIZE * 2) + "+")
        
        for row in range(BOARD_SIZE):
            print(f"{row} |", end="")
            for col in range(BOARD_SIZE):
                print(f" {self.board[row][col]}", end="")
            print(" |")
        
        print("  +" + "-" * (BOARD_SIZE * 2) + "+")
        print()

    def is_valid_move(self, start_row, start_col, target_row, target_col, player):
        """Check if a move from start to target position is valid."""
        # Checking the boundaries
        if not (0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE and 
                0 <= target_row < BOARD_SIZE and 0 <= target_col < BOARD_SIZE):
            return False
        
        # Selecting the own piece
        piece = self.board[start_row][start_col]
        if piece not in [player, player.lower()]:  # 'W','w' or 'B','b'
            return False

        row_diff = target_row - start_row
        col_diff = target_col - start_col

        # WHITE should move up (to smaller row numbers) unless it is a king
        if player == WHITE:
            if row_diff > 0 and piece == WHITE:  # WHITE can't move down (not king)
                return False
            
        else:  # BLACK should move down (to bigger row numbers) unless it is a king
            if row_diff < 0 and piece == BLACK:  # BLACK can't move up (not king)
                return False            

        # Diagonal move, even king moves the same number
        if abs(row_diff) not in (SIMPLE_MOVE, JUMP_MOVE) or abs(col_diff) not in (SIMPLE_MOVE, JUMP_MOVE) or abs(row_diff) != abs(col_diff):
            return False
        
        # Simple move
        if abs(row_diff) == SIMPLE_MOVE:
            if self.board[target_row][target_col] != EMPTY:  # target must be empty
                return False
            return True
        
        # When we have a jump
        if abs(row_diff) == JUMP_MOVE:
            if self.board[target_row][target_col] != EMPTY:  # target empty for landing
                return False
            # Enemy in the middle
            mid_row = (start_row + target_row) // 2
            mid_col = (start_col + target_col) // 2
            mid_piece = self.board[mid_row][mid_col]
            if mid_piece == EMPTY or mid_piece.upper() == player.upper():  # must be opponent
                return False
            return True
        
        return False

    def has_jump(self, player):
        """Check if the player has any available jump moves."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] in [player, player.lower()]:  # the player's piece
                    if self.has_jump_from_position(row, col, player):
                        return True
        return False

    def has_jump_from_position(self, row, col, player):
        """Check if a specific piece at (row, col) has any available jump moves.
        
        Note: Regular pieces cannot jump backwards, only kings can jump in all directions.
        """
        piece = self.board[row][col]
        if piece not in [player, player.lower()]:
            return False
        
        is_king = (piece.islower())  # Kings are lowercase
        
        for jump_row, jump_col in JUMP_DIRECTIONS:
            # Skip backward jumps for regular pieces
            if not is_king:
                if player == WHITE and jump_row > 0:  # WHITE can't jump down (backwards)
                    continue
                if player == BLACK and jump_row < 0:  # BLACK can't jump up (backwards)
                    continue
            
            new_row = row + jump_row
            new_col = col + jump_col
            
            # Check if target is valid and empty
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and self.board[new_row][new_col] == EMPTY:
                # Check for enemy in the middle
                middle_row = (row + new_row) // 2
                middle_col = (col + new_col) // 2
                enemy_there = self.board[middle_row][middle_col]
                
                if enemy_there != EMPTY and enemy_there.upper() != player.upper():
                    return True
        return False

    def has_any_legal_move(self, player):
        """Check if the player has any legal moves available.
        
        Respects mandatory jump rule: if any jumps exist, only jumps are legal moves.
        """
        # First check if any jumps are available
        jumps_available = self.has_jump(player)
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece not in [player, player.lower()]:
                    continue
                
                # If jumps are mandatory, only check for jumps
                if jumps_available:
                    if self.has_jump_from_position(row, col, player):
                        return True
                else:
                    # Check for simple moves (1 square diagonally)
                    is_king = piece.islower()
                    
                    # Try all 4 diagonal directions
                    for row_offset in [-1, 1]:
                        for col_offset in [-1, 1]:
                            # Skip backward moves for regular pieces
                            if not is_king:
                                if player == WHITE and row_offset > 0:  # WHITE can't move down
                                    continue
                                if player == BLACK and row_offset < 0:  # BLACK can't move up
                                    continue
                            
                            target_row = row + row_offset
                            target_col = col + col_offset
                            
                            if self.is_valid_move(row, col, target_row, target_col, player):
                                return True
        
        return False
                            

    def make_move(self, start_row, start_col, target_row, target_col, player):
        """Execute a move on the board if valid."""
        if not self.is_valid_move(start_row, start_col, target_row, target_col, player):
            return False
        
        piece = self.board[start_row][start_col]

        self.board[start_row][start_col] = EMPTY
        self.board[target_row][target_col] = piece

        # Handle jump (capture opponent piece)
        if abs(target_row - start_row) == JUMP_MOVE:
            mid_row = (start_row + target_row) // 2
            mid_col = (start_col + target_col) // 2
            self.board[mid_row][mid_col] = EMPTY

        # King promotion if it reaches the other end
        if piece == WHITE and target_row == 0:
            self.board[target_row][target_col] = WHITE_KING
        elif piece == BLACK and target_row == BOARD_SIZE - 1:
            self.board[target_row][target_col] = BLACK_KING
            
        return True
