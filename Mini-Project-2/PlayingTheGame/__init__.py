"""
PlayingTheGame Package - Game Controller for Checkers
"""

from GameBoard import GameBoard
from OtherStuff import WHITE, BLACK, AnalyticsManager
from SearchToolBox import MinimaxSearch, AlphaBetaSearch, AlphaBetaWithOrdering

class Checkers:
    """
    Game controller for checkers - supports 2 humans or human vs AI
    """

    def __init__(self):
        self.game_board = GameBoard()
        self.move_number = 0
        self.current_player = WHITE
        self.Analytics = AnalyticsManager()
    
    def StartingMoveLocation(self, X, Y):
        """Converts 1-indexed Line/Column to 0-indexed internal coordinates.
        
        Required by assignment naming convention.
        
        Args:
            X: Line number (1-8, user-facing)
            Y: Column number (1-8, user-facing)
        
        Returns:
            tuple: (Row, Col) in 0-indexed format
        """
        return X - 1, Y - 1
    
    def TargetingMoveLocation(self, X, Y):
        """Converts 1-indexed Line/Column to 0-indexed internal coordinates.
        
        Required by assignment naming convention.
        
        Args:
            X: Line number (1-8, user-facing)
            Y: Column number (1-8, user-facing)
        
        Returns:
            tuple: (Row, Col) in 0-indexed format
        """
        return X - 1, Y - 1
    
    def switch_player(self):
        if self.current_player == WHITE:
            self.current_player = BLACK
        else:
            self.current_player = WHITE

    def get_move_location(self):
        """Get starting and target locations for a move from user input."""
        while True:
            try:
                start_input = input(f'Player {self.current_player} Move # {self.move_number+1} - starting location (row col): ').strip()
                start_row, start_col = map(int, start_input.split())
                break
            except ValueError:
                print("ERROR: Please enter two numbers, for example: 6 1")

        while True:
            try:
                target_input = input(f'Enter Target Location (row col): ').strip()
                target_row, target_col = map(int, target_input.split())
                break
            except ValueError:
                print("ERROR: Please enter two numbers, for example: 6 1")
        
        return start_row, start_col, target_row, target_col
       
    def is_game_over(self):
        """Check if the game is over.
        
        Game ends when:
        1. One player has no pieces left (captured all)
        2. Current player has no legal moves (stalemate)
        
        Returns:
            bool - True if game is over, False otherwise
        """
        white_count = 0
        black_count = 0
        for row in self.game_board.board:
            for cell in row:
                if cell.upper() == WHITE:
                    white_count += 1
                elif cell.upper() == BLACK:
                    black_count += 1
        
        if white_count == 0:
            print(f"\n🏆 BLACK WINS! All white pieces captured.")
            print(f"Game ended after {self.move_number} moves.")
            return True
        if black_count == 0:
            print(f"\n🏆 WHITE WINS! All black pieces captured.")
            print(f"Game ended after {self.move_number} moves.")
            return True
        
        if not self.game_board.has_any_legal_move(self.current_player):
            winner = BLACK if self.current_player == WHITE else WHITE
            print(f"\n🏆 {winner} WINS! {self.current_player} has no legal moves (stalemate).")
            print(f"Game ended after {self.move_number} moves.")
            return True
        
        return False

        

    def play_human_turn(self):
        """Handle a single turn for the current human player.
        
        Handles multi-jump sequences: if a piece jumps and can jump again,
        the player must continue jumping with the same piece.
        """
        print(f"\n{'='*50}")
        print(f"Player {self.current_player} Turn # {self.move_number+1}")

        self.game_board.display_board()

        jumps_available = self.game_board.has_jump(self.current_player)
        if jumps_available:
            print(f"⚠ JUMP AVAILABLE! You must jump.")

        move_successful = False
        landing_row = None
        landing_col = None
        
        while not move_successful:
            start_row, start_col, target_row, target_col = self.get_move_location()

            if jumps_available:
                move_distance = abs(target_row - start_row)
                if move_distance == 1:
                    print("Invalid move: You must make a jump when one is available!")
                    continue
            
            result = self.game_board.make_move(start_row, start_col, target_row, target_col, self.current_player)
            if result['success']:
                landing_row = target_row
                landing_col = target_col
                move_successful = True
            else:
                print("Invalid move. Try again.")
        
        if result['was_jump']:
            if result['promoted']:
                print("Promoted to KING! Turn ends.")
                self.move_number += 1
                return
            
            while self.game_board.has_jump_from_position(landing_row, landing_col, self.current_player):
                print("\n" + "="*50)
                print(f"⚠ ADDITIONAL JUMP AVAILABLE! You must continue jumping.")
                self.game_board.display_board()
                
                jump_made = False
                while not jump_made:
                    start_row, start_col, target_row, target_col = self.get_move_location()
                    
                    if start_row != landing_row or start_col != landing_col:
                        print(f"Invalid: You must continue jumping with the piece at ({landing_row}, {landing_col})!")
                        continue
                    
                    if abs(target_row - start_row) != 2:
                        print("Invalid: You must make a jump (distance of 2)!")
                        continue
                    
                    result = self.game_board.make_move(start_row, start_col, target_row, target_col, self.current_player)
                    if result['success']:
                        landing_row = target_row
                        landing_col = target_col
                        jump_made = True
                    else:
                        print("Invalid move. Try again.")
                
                if result['promoted']:
                    print("Promoted to KING! Turn ends.")
                    break
        
        self.move_number += 1
        print(f"\nTurn complete! Total moves: {self.move_number}")
        
    def play_game_two_players(self):
        """Main game loop for two human players."""
        while True:
            if self.is_game_over():
                break
            
            self.play_human_turn()
            self.switch_player()
    
        print("\nGAME OVER!")
        self.game_board.display_board()
    
    def play_ai_turn(self, search_algorithm):
        """Handle a single turn for the AI player.
        
        Note: This simplified version only handles single moves.
        Multi-jump sequences for AI will be handled by the search algorithm.
        
        Args:
            search_algorithm: Instance of MinimaxSearch, AlphaBetaSearch, or AlphaBetaWithOrdering
        """
        print(f"\n{'='*50}")
        print(f"AI Player {self.current_player} Turn # {self.move_number+1}")
        print("Thinking...")
        
        self.game_board.display_board()
        
        # Get best move from AI
        best_move = search_algorithm.GetBestMove(self.game_board, self.current_player)
        
        if best_move is None:
            print("AI has no legal moves!")
            self.move_number += 1
            return
        
        # Extract move information
        start_row, start_col = best_move.StartingMoveLocation
        target_row, target_col = best_move.DestinationLocation
        
        print(f"AI moves from ({start_row}, {start_col}) to ({target_row}, {target_col})")
        
        # Execute the move
        result = self.game_board.make_move(start_row, start_col, target_row, target_col, self.current_player)
        
        if result['success']:
            if result['promoted']:
                print("AI piece promoted to KING!")
            if result['was_jump']:
                print("AI captured an opponent piece!")
        
        # Record analytics
        ai_metrics = {
            "NumberNodesExpanded": search_algorithm.Analytics.NumberNodesExpanded,
            "NumberPrunes": search_algorithm.Analytics.NumberNodesPruned,
            "NumberOrderedPrunes": search_algorithm.Analytics.NumberNodesPruned if 'Ordering' in search_algorithm.Analytics.SearchStrategy else 0,
            "EffectiveDepthReached": search_algorithm.Analytics.MaxDepthReached,
            "LastSearchMillis": int(search_algorithm.Analytics.GetTimeElapsed() * 1000),
            "Strategy": search_algorithm.Analytics.SearchStrategy,
            "TimeLimitSeconds": search_algorithm.TimeLimit,
            "MaxPlies": search_algorithm.MaxDepth,
        }
        self.Analytics.RecordMoveAnalytics("black", ai_metrics, best_move.Describe())
        self.Analytics.PrintLastMoveAnalytics()
        
        self.move_number += 1
        print(f"\nAI turn complete! Total moves: {self.move_number}")
    
    def play_game_human_vs_ai(self, SearchStrategy='AlphaBetaOrdering', MaxDepth=7, TimeLimit=3.0):
        """Main game loop for human (WHITE) vs AI (BLACK).
        
        Args:
            SearchStrategy: 'Minimax', 'AlphaBeta', or 'AlphaBetaOrdering'
            MaxDepth: Maximum search depth (plies) - recommended 5-9
            TimeLimit: Maximum time for AI to think (seconds)
        """
        print("\n" + "="*60)
        print("CHECKERS: HUMAN (WHITE) vs AI (BLACK)")
        print("="*60)
        print(f"AI Strategy: {SearchStrategy}")
        print(f"Max Depth: {MaxDepth} plies")
        print(f"Time Limit: {TimeLimit} seconds")
        print("="*60 + "\n")
        
        # Initialize AI search algorithm
        if SearchStrategy == 'Minimax':
            ai_search = MinimaxSearch(MaxDepth, TimeLimit)
        elif SearchStrategy == 'AlphaBeta':
            ai_search = AlphaBetaSearch(MaxDepth, TimeLimit)
        elif SearchStrategy == 'AlphaBetaOrdering':
            ai_search = AlphaBetaWithOrdering(MaxDepth, TimeLimit)
        else:
            print(f"Unknown search strategy: {SearchStrategy}. Using AlphaBetaOrdering.")
            ai_search = AlphaBetaWithOrdering(MaxDepth, TimeLimit)
        
        # Set initial player to WHITE (human goes first)
        self.current_player = WHITE
        
        while True:
            if self.is_game_over():
                break
            
            # Human's turn (WHITE)
            if self.current_player == WHITE:
                self.play_human_turn()
            # AI's turn (BLACK)
            else:
                self.play_ai_turn(ai_search)
            
            self.switch_player()
        
        print("\n" + "="*60)
        print("GAME OVER!")
        print("="*60)
        self.game_board.display_board()
