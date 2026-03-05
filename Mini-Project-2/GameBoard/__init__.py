"""
GameBoard Package - Board State and Move Validation for Checkers
"""

from OtherStuff import (BOARD_SIZE, WHITE, BLACK, WHITE_KING, BLACK_KING, EMPTY,
                        BLACK_ROWS, WHITE_ROWS, SIMPLE_MOVE, JUMP_MOVE, JUMP_DIRECTIONS)

class GameBoard:
    def __init__(self):
        self.board = []
        for row_number in range(BOARD_SIZE):
            one_row = []
            for col_number in range(BOARD_SIZE):
                one_row.append(EMPTY)
            
            self.board.append(one_row)

        self.setup_initial_board()


    def setup_initial_board(self):
        """Set up the initial checker pieces on the board."""
        for row in BLACK_ROWS:
            for col in range(BOARD_SIZE):
                if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                    self.board[row][col] = BLACK

        for row in WHITE_ROWS:
            for col in range(BOARD_SIZE):
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
        if not (0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE and 
                0 <= target_row < BOARD_SIZE and 0 <= target_col < BOARD_SIZE):
            return False
        
        piece = self.board[start_row][start_col]
        if piece not in [player, player.lower()]:
            return False

        row_diff = target_row - start_row
        col_diff = target_col - start_col

        if player == WHITE:
            if row_diff > 0 and piece == WHITE:
                return False
        else:
            if row_diff < 0 and piece == BLACK:
                return False

        if abs(row_diff) not in (SIMPLE_MOVE, JUMP_MOVE) or abs(col_diff) not in (SIMPLE_MOVE, JUMP_MOVE) or abs(row_diff) != abs(col_diff):
            return False
        
        if abs(row_diff) == SIMPLE_MOVE:
            if self.board[target_row][target_col] != EMPTY:
                return False
            return True
        
        if abs(row_diff) == JUMP_MOVE:
            if self.board[target_row][target_col] != EMPTY:
                return False
            
            mid_row = (start_row + target_row) // 2
            mid_col = (start_col + target_col) // 2
            mid_piece = self.board[mid_row][mid_col]
            if mid_piece == EMPTY or mid_piece.upper() == player.upper():
                return False
            return True
        
        return False

    def _is_king(self, piece):
        """Check if a piece is a king (kings are lowercase: 'w' or 'b')."""
        return piece.islower()
    
    def _is_backward_direction(self, player, row_offset):
        """Check if a move direction is backwards for a regular (non-king) piece.
        
        WHITE pieces move up (negative row offset), so positive offset is backwards.
        BLACK pieces move down (positive row offset), so negative offset is backwards.
        """
        if player == WHITE:
            return row_offset > 0
        else:
            return row_offset < 0
    
    def _can_jump_in_direction(self, row, col, row_offset, col_offset, player):
        """Check if a piece can jump in a specific direction.
        
        Returns True if:
        - Target square is on board and empty
        - Middle square contains an enemy piece
        - Direction is valid for piece type (kings can go any direction)
        """
        piece = self.board[row][col]
        
        if not self._is_king(piece) and self._is_backward_direction(player, row_offset):
            return False
        
        target_row = row + row_offset
        target_col = col + col_offset
        middle_row = (row + target_row) // 2
        middle_col = (col + target_col) // 2
        
        if not (0 <= target_row < BOARD_SIZE and 0 <= target_col < BOARD_SIZE):
            return False
        if self.board[target_row][target_col] != EMPTY:
            return False
        
        middle_piece = self.board[middle_row][middle_col]
        if middle_piece == EMPTY or middle_piece.upper() == player.upper():
            return False
        
        return True

    def has_jump_from_position(self, row, col, player):
        """Check if the piece at (row, col) can jump to capture an opponent.
        
        Returns True if at least one jump is available from this position.
        """
        piece = self.board[row][col]
        if piece not in [player, player.lower()]:
            return False
        
        for row_offset, col_offset in JUMP_DIRECTIONS:
            if self._can_jump_in_direction(row, col, row_offset, col_offset, player):
                return True
        return False

    def has_jump(self, player):
        """Check if the player has any pieces that can make a jump.
        
        Returns True if at least one jump is available anywhere on the board.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece in [player, player.lower()]:
                    if self.has_jump_from_position(row, col, player):
                        return True
        return False

    def has_any_legal_move(self, player):
        """Check if the player has any legal moves available.
        
        Respects mandatory jump rule: if any jumps exist, only jumps are legal moves.
        Returns True if at least one legal move exists, False otherwise (stalemate).
        """
        jumps_available = self.has_jump(player)
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece not in [player, player.lower()]:
                    continue
                
                if jumps_available:
                    if self.has_jump_from_position(row, col, player):
                        return True
                else:
                    for row_offset in [-1, 1]:
                        for col_offset in [-1, 1]:
                            if not self._is_king(piece) and self._is_backward_direction(player, row_offset):
                                continue
                            
                            target_row = row + row_offset
                            target_col = col + col_offset
                            
                            if self.is_valid_move(row, col, target_row, target_col, player):
                                return True
        
        return False
                            

    def make_move(self, start_row, start_col, target_row, target_col, player):
        """Execute a move on the board if valid.
        
        Returns:
            dict with keys:
                - 'success': bool - whether move was executed
                - 'was_jump': bool - whether move was a jump (captured opponent)
                - 'promoted': bool - whether piece was promoted to king
        """
        if not self.is_valid_move(start_row, start_col, target_row, target_col, player):
            return {'success': False, 'was_jump': False, 'promoted': False}
        
        piece = self.board[start_row][start_col]
        was_jump = abs(target_row - start_row) == JUMP_MOVE

        self.board[start_row][start_col] = EMPTY
        self.board[target_row][target_col] = piece

        if was_jump:
            mid_row = (start_row + target_row) // 2
            mid_col = (start_col + target_col) // 2
            self.board[mid_row][mid_col] = EMPTY

        promoted = False
        if piece == WHITE and target_row == 0:
            self.board[target_row][target_col] = WHITE_KING
            promoted = True
        elif piece == BLACK and target_row == BOARD_SIZE - 1:
            self.board[target_row][target_col] = BLACK_KING
            promoted = True
            
        return {'success': True, 'was_jump': was_jump, 'promoted': promoted}
