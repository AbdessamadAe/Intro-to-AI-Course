"""
SearchToolBox Package - AI Search Algorithms for Checkers

This package contains:
- Minimax search algorithm
- Alpha-Beta pruning
- Alpha-Beta with move ordering
- Evaluation heuristic for board states
"""

import copy
import time
from OtherStuff import (WHITE, BLACK, WHITE_KING, BLACK_KING, EMPTY, BOARD_SIZE,
                       MoveRepresentation, AnalyticsTracker)


def EvaluateBoardState(game_board, player):
    """Evaluate the board state from the perspective of the given player.
    
    Higher scores are better for the player.
    
    Evaluation components:
    - Material: Regular pieces = 3 points, Kings = 5 points
    - Position: Pieces closer to being kinged = bonus points
    - Center control: Pieces in center squares = bonus points
    - Mobility: Number of legal moves available
    
    Args:
        game_board: GameBoard instance
        player: Player to evaluate for (WHITE or BLACK)
    
    Returns:
        float: Evaluation score (positive = good for player, negative = bad)
    """
    opponent = BLACK if player == WHITE else WHITE
    
    player_score = 0
    opponent_score = 0
    
    # Material and positional evaluation
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = game_board.board[row][col]
            
            if piece == EMPTY:
                continue
            
            # Determine piece value
            if piece.upper() == WHITE:
                piece_value = 3.0  # Regular piece
                is_king = piece == WHITE_KING
                piece_owner = WHITE
            elif piece.upper() == BLACK:
                piece_value = 3.0  # Regular piece
                is_king = piece == BLACK_KING
                piece_owner = BLACK
            else:
                continue
            
            # King bonus
            if is_king:
                piece_value = 5.0
            else:
                # Positional bonus - reward pieces closer to promotion
                if piece_owner == WHITE:
                    # WHITE moves toward row 0
                    advancement = (BOARD_SIZE - 1 - row) / (BOARD_SIZE - 1)
                else:
                    # BLACK moves toward row 7
                    advancement = row / (BOARD_SIZE - 1)
                piece_value += advancement * 0.5
            
            # Center control bonus
            center_distance = abs(row - 3.5) + abs(col - 3.5)
            center_bonus = (7.0 - center_distance) * 0.1
            piece_value += center_bonus
            
            # Add to appropriate player's score
            if piece_owner == player:
                player_score += piece_value
            else:
                opponent_score += piece_value
    
    # Mobility evaluation (number of legal moves)
    player_mobility = len(GetAllLegalMoves(game_board, player))
    opponent_mobility = len(GetAllLegalMoves(game_board, opponent))
    
    mobility_score = (player_mobility - opponent_mobility) * 0.2
    
    return player_score - opponent_score + mobility_score


def GetAllLegalMoves(game_board, player):
    """Get all legal moves for a player.
    
    Respects mandatory jump rule.
    
    Args:
        game_board: GameBoard instance
        player: Player to get moves for
    
    Returns:
        list: List of MoveRepresentation objects
    """
    moves = []
    
    # Check if jumps are available (mandatory)
    jumps_available = game_board.has_jump(player)
    
    for start_row in range(BOARD_SIZE):
        for start_col in range(BOARD_SIZE):
            piece = game_board.board[start_row][start_col]
            
            # Skip if not player's piece
            if piece not in [player, player.lower()]:
                continue
            
            # If jumps are available, only consider jump moves
            if jumps_available:
                # Check all jump directions
                for row_offset in [-2, 2]:
                    for col_offset in [-2, 2]:
                        target_row = start_row + row_offset
                        target_col = start_col + col_offset
                        
                        if game_board.is_valid_move(start_row, start_col, target_row, target_col, player):
                            move = MoveRepresentation(
                                (start_row, start_col),
                                (target_row, target_col)
                            )
                            moves.append(move)
            else:
                # No jumps available, consider all simple moves
                for row_offset in [-1, 1]:
                    for col_offset in [-1, 1]:
                        target_row = start_row + row_offset
                        target_col = start_col + col_offset
                        
                        if game_board.is_valid_move(start_row, start_col, target_row, target_col, player):
                            move = MoveRepresentation(
                                (start_row, start_col),
                                (target_row, target_col)
                            )
                            moves.append(move)
                
                # Also check jump moves
                for row_offset in [-2, 2]:
                    for col_offset in [-2, 2]:
                        target_row = start_row + row_offset
                        target_col = start_col + col_offset
                        
                        if game_board.is_valid_move(start_row, start_col, target_row, target_col, player):
                            move = MoveRepresentation(
                                (start_row, start_col),
                                (target_row, target_col)
                            )
                            moves.append(move)
    
    return moves


def ApplyMove(game_board, move):
    """Apply a move to a board and return the new board state.
    
    Args:
        game_board: GameBoard instance
        move: MoveRepresentation object
    
    Returns:
        GameBoard: New board state after move
    """
    new_board = copy.deepcopy(game_board)
    start_row, start_col = move.StartingMoveLocation
    target_row, target_col = move.DestinationLocation
    
    piece = new_board.board[start_row][start_col]
    player = piece.upper()
    
    new_board.make_move(start_row, start_col, target_row, target_col, player)
    
    return new_board


def IsTerminalState(game_board, player):
    """Check if the game has reached a terminal state.
    
    Args:
        game_board: GameBoard instance
        player: Current player
    
    Returns:
        bool: True if terminal state (game over)
    """
    # Check if player has any pieces
    player_has_pieces = False
    opponent = BLACK if player == WHITE else WHITE
    opponent_has_pieces = False
    
    for row in game_board.board:
        for cell in row:
            if cell.upper() == player:
                player_has_pieces = True
            if cell.upper() == opponent:
                opponent_has_pieces = True
    
    if not player_has_pieces or not opponent_has_pieces:
        return True
    
    # Check if player has any legal moves
    if not game_board.has_any_legal_move(player):
        return True
    
    return False


class MinimaxSearch:
    """Minimax search algorithm for checkers."""
    
    def __init__(self, MaxDepth, TimeLimit=3.0):
        """
        Args:
            MaxDepth: Maximum search depth (plies)
            TimeLimit: Maximum time for search in seconds
        """
        self.MaxDepth = MaxDepth
        self.TimeLimit = TimeLimit
        self.Analytics = AnalyticsTracker('Minimax')
    
    def GetBestMove(self, game_board, player):
        """Find the best move using Minimax algorithm.
        
        Args:
            game_board: Current GameBoard instance
            player: Player to find move for (AI player)
        
        Returns:
            MoveRepresentation: Best move found, or None if no moves available
        """
        self.Analytics.Reset()
        self.Analytics.StartTimer()
        start_time = time.time()
        deadline = start_time + self.TimeLimit
        
        best_move = None
        best_value = float('-inf')
        
        legal_moves = GetAllLegalMoves(game_board, player)
        
        if not legal_moves:
            self.Analytics.StopTimer()
            return None
        
        for move in legal_moves:
            if time.time() >= deadline:
                break
            new_board = ApplyMove(game_board, move)
            
            move_value = self._MinimaxRecursive(
                new_board,
                self.MaxDepth - 1,
                False,
                player,
                deadline
            )
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        self.Analytics.StopTimer()
        return best_move
    
    def _MinimaxRecursive(self, game_board, depth, is_maximizing, ai_player, deadline):
        """Recursive Minimax implementation.
        
        Args:
            game_board: Current board state
            depth: Remaining depth to search
            is_maximizing: True if maximizing player's turn
            ai_player: The AI player (for evaluation)
            deadline: Time deadline for search termination
        
        Returns:
            float: Evaluation score
        """
        # Check time limit
        if time.time() >= deadline:
            return EvaluateBoardState(game_board, ai_player)
        
        self.Analytics.IncrementNodesExpanded()
        self.Analytics.UpdateMaxDepth(self.MaxDepth - depth)
        
        current_player = ai_player if is_maximizing else (BLACK if ai_player == WHITE else WHITE)
        
        # Terminal conditions
        if depth == 0 or IsTerminalState(game_board, current_player):
            return EvaluateBoardState(game_board, ai_player)
        
        legal_moves = GetAllLegalMoves(game_board, current_player)
        
        if not legal_moves:
            return EvaluateBoardState(game_board, ai_player)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = ApplyMove(game_board, move)
                eval_score = self._MinimaxRecursive(new_board, depth - 1, False, ai_player, deadline)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = ApplyMove(game_board, move)
                eval_score = self._MinimaxRecursive(new_board, depth - 1, True, ai_player, deadline)
                min_eval = min(min_eval, eval_score)
            return min_eval


class AlphaBetaSearch:
    """Alpha-Beta pruning search algorithm for checkers."""
    
    def __init__(self, MaxDepth, TimeLimit=3.0):
        """
        Args:
            MaxDepth: Maximum search depth (plies)
            TimeLimit: Maximum time for search in seconds
        """
        self.MaxDepth = MaxDepth
        self.TimeLimit = TimeLimit
        self.Analytics = AnalyticsTracker('AlphaBeta')
    
    def GetBestMove(self, game_board, player):
        """Find the best move using Alpha-Beta pruning.
        
        Args:
            game_board: Current GameBoard instance
            player: Player to find move for (AI player)
        
        Returns:
            MoveRepresentation: Best move found, or None if no moves available
        """
        self.Analytics.Reset()
        self.Analytics.StartTimer()
        start_time = time.time()
        deadline = start_time + self.TimeLimit
        
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        legal_moves = GetAllLegalMoves(game_board, player)
        
        if not legal_moves:
            self.Analytics.StopTimer()
            return None
        
        for move in legal_moves:
            if time.time() >= deadline:
                break
            new_board = ApplyMove(game_board, move)
            
            move_value = self._AlphaBetaRecursive(
                new_board,
                self.MaxDepth - 1,
                alpha,
                beta,
                False,
                player,
                deadline
            )
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
            
            alpha = max(alpha, best_value)
        
        self.Analytics.StopTimer()
        return best_move
    
    def _AlphaBetaRecursive(self, game_board, depth, alpha, beta, is_maximizing, ai_player, deadline):
        """Recursive Alpha-Beta implementation.
        
        Args:
            game_board: Current board state
            depth: Remaining depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player's turn
            ai_player: The AI player (for evaluation)
            deadline: Time deadline for search termination
        
        Returns:
            float: Evaluation score
        """
        # Check time limit
        if time.time() >= deadline:
            return EvaluateBoardState(game_board, ai_player)
        
        self.Analytics.IncrementNodesExpanded()
        self.Analytics.UpdateMaxDepth(self.MaxDepth - depth)
        
        current_player = ai_player if is_maximizing else (BLACK if ai_player == WHITE else WHITE)
        
        # Terminal conditions
        if depth == 0 or IsTerminalState(game_board, current_player):
            return EvaluateBoardState(game_board, ai_player)
        
        legal_moves = GetAllLegalMoves(game_board, current_player)
        
        if not legal_moves:
            return EvaluateBoardState(game_board, ai_player)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = ApplyMove(game_board, move)
                eval_score = self._AlphaBetaRecursive(new_board, depth - 1, alpha, beta, False, ai_player, deadline)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.Analytics.IncrementNodesPruned()
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = ApplyMove(game_board, move)
                eval_score = self._AlphaBetaRecursive(new_board, depth - 1, alpha, beta, True, ai_player, deadline)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.Analytics.IncrementNodesPruned()
                    break  # Alpha cutoff
            return min_eval


class AlphaBetaWithOrdering:
    """Alpha-Beta pruning with move ordering for improved pruning."""
    
    def __init__(self, MaxDepth, TimeLimit=3.0):
        """
        Args:
            MaxDepth: Maximum search depth (plies)
            TimeLimit: Maximum time for search in seconds
        """
        self.MaxDepth = MaxDepth
        self.TimeLimit = TimeLimit
        self.Analytics = AnalyticsTracker('AlphaBetaOrdering')
    
    def GetBestMove(self, game_board, player):
        """Find the best move using Alpha-Beta with move ordering.
        
        Args:
            game_board: Current GameBoard instance
            player: Player to find move for (AI player)
        
        Returns:
            MoveRepresentation: Best move found, or None if no moves available
        """
        self.Analytics.Reset()
        self.Analytics.StartTimer()
        start_time = time.time()
        deadline = start_time + self.TimeLimit
        
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        legal_moves = GetAllLegalMoves(game_board, player)
        
        if not legal_moves:
            self.Analytics.StopTimer()
            return None
        
        # Order moves for better pruning
        ordered_moves = self._OrderMoves(game_board, legal_moves, player)
        
        for move in ordered_moves:
            if time.time() >= deadline:
                break
            new_board = ApplyMove(game_board, move)
            
            move_value = self._AlphaBetaRecursive(
                new_board,
                self.MaxDepth - 1,
                alpha,
                beta,
                False,
                player,
                deadline
            )
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
            
            alpha = max(alpha, best_value)
        
        self.Analytics.StopTimer()
        return best_move
    
    def _OrderMoves(self, game_board, moves, player):
        """Order moves by likely best-first (for better pruning).
        
        Heuristics:
        - Jumps (captures) first
        - Moves that create kings
        - Moves toward center
        - Moves toward promotion
        
        Args:
            game_board: Current board state
            moves: List of MoveRepresentation objects
            player: Player making the moves
        
        Returns:
            list: Ordered list of moves
        """
        def move_priority(move):
            start_row, start_col = move.StartingMoveLocation
            target_row, target_col = move.DestinationLocation
            
            priority = 0
            
            # Jumps (captures) are highest priority
            if abs(target_row - start_row) == 2:
                priority += 100
            
            # King promotion
            if player == WHITE and target_row == 0:
                priority += 50
            elif player == BLACK and target_row == BOARD_SIZE - 1:
                priority += 50
            
            # Center control
            center_distance = abs(target_row - 3.5) + abs(target_col - 3.5)
            priority += (7.0 - center_distance)
            
            # Advancement toward promotion
            if player == WHITE:
                priority += (BOARD_SIZE - target_row)
            else:
                priority += target_row
            
            return priority
        
        return sorted(moves, key=move_priority, reverse=True)
    
    def _AlphaBetaRecursive(self, game_board, depth, alpha, beta, is_maximizing, ai_player, deadline):
        """Recursive Alpha-Beta implementation with move ordering.
        
        Args:
            game_board: Current board state
            depth: Remaining depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player's turn
            ai_player: The AI player (for evaluation)
            deadline: Time deadline for search termination
        
        Returns:
            float: Evaluation score
        """
        # Check time limit
        if time.time() >= deadline:
            return EvaluateBoardState(game_board, ai_player)
        
        self.Analytics.IncrementNodesExpanded()
        self.Analytics.UpdateMaxDepth(self.MaxDepth - depth)
        
        current_player = ai_player if is_maximizing else (BLACK if ai_player == WHITE else WHITE)
        
        # Terminal conditions
        if depth == 0 or IsTerminalState(game_board, current_player):
            return EvaluateBoardState(game_board, ai_player)
        
        legal_moves = GetAllLegalMoves(game_board, current_player)
        
        if not legal_moves:
            return EvaluateBoardState(game_board, ai_player)
        
        # Order moves for better pruning
        ordered_moves = self._OrderMoves(game_board, legal_moves, current_player)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in ordered_moves:
                new_board = ApplyMove(game_board, move)
                eval_score = self._AlphaBetaRecursive(new_board, depth - 1, alpha, beta, False, ai_player, deadline)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.Analytics.IncrementNodesPruned()
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in ordered_moves:
                new_board = ApplyMove(game_board, move)
                eval_score = self._AlphaBetaRecursive(new_board, depth - 1, alpha, beta, True, ai_player, deadline)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.Analytics.IncrementNodesPruned()
                    break  # Alpha cutoff
            return min_eval

