"""
Constants for the Checkers game.
"""

# Board dimensions
BOARD_SIZE = 8

# Piece representations
WHITE = 'W'
BLACK = 'B'
WHITE_KING = 'w'
BLACK_KING = 'b'
EMPTY = '.'

# Initial board setup rows
BLACK_ROWS = (0, 1, 2)  # Black pieces start in top 3 rows
WHITE_ROWS = (5, 6, 7)  # White pieces start in bottom 3 rows

# Move distances
SIMPLE_MOVE = 1
JUMP_MOVE = 2

# Jump directions (row_offset, col_offset)
JUMP_DIRECTIONS = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
