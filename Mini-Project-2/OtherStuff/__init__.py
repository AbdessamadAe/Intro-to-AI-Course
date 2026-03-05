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
    
    def Describe(self):
        """Returns a text description of the move.
        
        Converts 0-indexed coordinates to 1-indexed for display.
        """
        start_row, start_col = self.StartingMoveLocation
        end_row, end_col = self.DestinationLocation
        return f"({start_row+1},{start_col+1}) -> ({end_row+1},{end_col+1})"


class AnalyticsTracker:
    """Tracks analytics for a single AI search."""
    
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


class AnalyticsManager:
    """Tracks cumulative analytics across all moves for both players."""
    
    def __init__(self):
        self.CumulativeWhite = {
            "NumberNodesExpanded": 0,
            "NumberPrunes": 0,
            "TotalMoves": 0,
            "MaxDepthReached": 0,
        }
        self.CumulativeBlack = {
            "NumberNodesExpanded": 0,
            "NumberPrunes": 0,
            "TotalMoves": 0,
            "MaxDepthReached": 0,
        }
        self.PerMoveReports = []
    
    def RecordMoveAnalytics(self, Player, Metrics, MoveText):
        """Record per-move analytics and update cumulative stats.
        
        Args:
            Player: 'white' or 'black'
            Metrics: Dict with NumberNodesExpanded, NumberPrunes, etc.
            MoveText: String description of the move
        """
        report = {
            "Player": Player,
            "MoveText": MoveText,
            "NumberNodesExpanded": Metrics.get("NumberNodesExpanded", 0),
            "NumberPrunes": Metrics.get("NumberPrunes", 0),
            "MaxDepthReached": Metrics.get("MaxDepthReached", 0),
            "LastSearchMillis": Metrics.get("LastSearchMillis", 0),
            "Strategy": Metrics.get("Strategy", "Unknown"),
        }
        self.PerMoveReports.append(report)
        
        cum = self.CumulativeWhite if Player == "white" else self.CumulativeBlack
        cum["NumberNodesExpanded"] += report["NumberNodesExpanded"]
        cum["NumberPrunes"] += report["NumberPrunes"]
        cum["TotalMoves"] += 1
        cum["MaxDepthReached"] = max(cum["MaxDepthReached"], report["MaxDepthReached"])
    
    def PrintLastMoveAnalytics(self):
        """Print analytics for the last move."""
        if not self.PerMoveReports:
            return
        rpt = self.PerMoveReports[-1]
        print("\nAnalytics for this move:")
        print(f"- Player: {rpt['Player']}")
        print(f"- Move: {rpt['MoveText']}")
        print(f"- States expanded: {rpt['NumberNodesExpanded']}")
        print(f"- Prunes: {rpt['NumberPrunes']}")
        print(f"- Max depth: {rpt['MaxDepthReached']}")
        print(f"- Search time: {rpt['LastSearchMillis']} ms")
        print(f"- Strategy: {rpt['Strategy']}")
    
    def PrintCumulativeAnalytics(self):
        """Print cumulative analytics for both players."""
        print("\n" + "="*60)
        print("CUMULATIVE ANALYTICS")
        print("="*60)
        print("\nWhite:")
        self._PrintCumulative(self.CumulativeWhite)
        print("\nBlack:")
        self._PrintCumulative(self.CumulativeBlack)
        print("="*60)
    
    def _PrintCumulative(self, cum):
        """Helper to print cumulative stats for one player."""
        print(f"  Moves: {cum['TotalMoves']}")
        print(f"  States expanded: {cum['NumberNodesExpanded']}")
        print(f"  Prunes: {cum['NumberPrunes']}")
        print(f"  Max depth reached: {cum['MaxDepthReached']}")
