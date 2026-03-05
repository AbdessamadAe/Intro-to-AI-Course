"""
OtherStuff Package - Constants, Utilities, and Analytics for Checkers Game
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
BLACK_ROWS = (0, 1, 2)
WHITE_ROWS = (5, 6, 7)

# Move distances
SIMPLE_MOVE = 1
JUMP_MOVE = 2

# Jump directions (row_offset, col_offset)
JUMP_DIRECTIONS = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
