"""
SearchToolBox Package - AI Search Algorithms for Checkers

This package will contain:
- Minimax search algorithm
- Alpha-Beta pruning
- Alpha-Beta with move ordering
- Evaluation heuristic for board states
"""

# AI search algorithms will be implemented here

class SearchAlgorithm:
    """Base class for search algorithms (to be implemented)."""
    
    def __init__(self):
        pass
    
    def get_best_move(self, game_board, player, depth):
        """Find the best move for the given player.
        
        Args:
            game_board: Current GameBoard instance
            player: Current player (WHITE or BLACK)
            depth: Maximum search depth (look-ahead plies)
        
        Returns:
            tuple: (start_row, start_col, target_row, target_col)
        """
        raise NotImplementedError("Subclasses must implement get_best_move()")
