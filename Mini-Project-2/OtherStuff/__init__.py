"""
OtherStuff Package - Constants, Utilities, and Analytics for Checkers Game
"""

import time
import copy

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


class GameMove:
    """Represents a move in the checkers game."""
    
    def __init__(self, StartingMoveLocation, DestinationLocation):
        """
        Args:
            StartingMoveLocation: tuple (row, col) of starting position
            DestinationLocation: tuple (row, col) of destination position
        """
        self.StartingMoveLocation = StartingMoveLocation
        self.DestinationLocation = DestinationLocation
    
    def __repr__(self):
        return f"Move({self.StartingMoveLocation} -> {self.DestinationLocation})"
    
    def __eq__(self, other):
        if not isinstance(other, GameMove):
            return False
        return (self.StartingMoveLocation == other.StartingMoveLocation and 
                self.DestinationLocation == other.DestinationLocation)


class AnalyticsTracker:
    """Tracks analytics for AI search algorithms."""
    
    def __init__(self, SearchStrategy):
        """
        Args:
            SearchStrategy: String name of the search strategy being used
                           ('Minimax', 'AlphaBeta', 'AlphaBetaOrdering')
        """
        self.SearchStrategy = SearchStrategy
        self.NumberNodesExpanded = 0
        self.NumberNodesPruned = 0
        self.StartTime = None
        self.EndTime = None
        self.MaxDepthReached = 0
        self.MoveOrderingImprovement = 0
        
    def StartTimer(self):
        """Start timing the search."""
        self.StartTime = time.time()
    
    def StopTimer(self):
        """Stop timing the search."""
        self.EndTime = time.time()
    
    def IncrementNodesExpanded(self):
        """Increment the count of nodes expanded."""
        self.NumberNodesExpanded += 1
    
    def IncrementNodesPruned(self):
        """Increment the count of nodes pruned."""
        self.NumberNodesPruned += 1
        
    def UpdateMaxDepth(self, depth):
        """Update the maximum depth reached."""
        if depth > self.MaxDepthReached:
            self.MaxDepthReached = depth
    
    def GetTimeElapsed(self):
        """Get the time elapsed in seconds."""
        if self.StartTime is None or self.EndTime is None:
            return 0.0
        return self.EndTime - self.StartTime
    
    def GetSpaceComplexity(self):
        """Estimate space complexity (max depth reached)."""
        return self.MaxDepthReached
    
    def Reset(self):
        """Reset all analytics counters."""
        self.NumberNodesExpanded = 0
        self.NumberNodesPruned = 0
        self.StartTime = None
        self.EndTime = None
        self.MaxDepthReached = 0
        self.MoveOrderingImprovement = 0
    
    def PrintAnalytics(self):
        """Print analytics report."""
        print(f"\n{'='*60}")
        print(f"Search Analytics - {self.SearchStrategy}")
        print(f"{'='*60}")
        print(f"Nodes Expanded:     {self.NumberNodesExpanded}")
        if self.SearchStrategy in ['AlphaBeta', 'AlphaBetaOrdering']:
            print(f"Nodes Pruned:       {self.NumberNodesPruned}")
            pruning_percentage = (self.NumberNodesPruned / max(1, self.NumberNodesExpanded + self.NumberNodesPruned)) * 100
            print(f"Pruning Efficiency: {pruning_percentage:.1f}%")
        print(f"Max Depth Reached:  {self.MaxDepthReached}")
        print(f"Time Elapsed:       {self.GetTimeElapsed():.4f} seconds")
        print(f"Space Complexity:   O({self.GetSpaceComplexity()})")
        print(f"{'='*60}\n")
