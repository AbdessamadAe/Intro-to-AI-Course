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


def save_game_log(log_data, log_dir=None):
    """Save a structured game analytics log to a timestamped text file.

    Args:
        log_data (dict): Keys:
            mode        - 'Human vs Human' or 'Human vs AI'
            interface   - 'Console' or 'GUI'
            winner      - 'WHITE', 'BLACK', or None
            total_moves - int
            move_history- list of str
            ai_config   - dict with strategy/depth/time_limit, or None
            ai_move_logs- list of dicts (nodes, prunes, depth, time, move_text)
        log_dir (str): Directory to save logs; defaults to analytics-logs/ inside project root.
    """
    import os
    from datetime import datetime

    if log_dir is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(project_root, 'analytics-logs')

    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now()
    filename = timestamp.strftime('game_%Y%m%d_%H%M%S.txt')
    filepath = os.path.join(log_dir, filename)

    sep  = '=' * 60
    dash = '-' * 60

    lines = []
    lines += [sep, 'CHECKERS GAME LOG', sep]
    lines += [f"Date/Time:    {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"]
    lines += [f"Mode:         {log_data.get('mode', 'Unknown')}"]
    lines += [f"Interface:    {log_data.get('interface', 'Unknown')}"]

    ai_config = log_data.get('ai_config')
    if ai_config:
        lines += ['', 'AI Configuration:']
        lines += [f"  Strategy:   {ai_config.get('strategy', '?')}"]
        lines += [f"  Max Depth:  {ai_config.get('depth', '?')}"]
        lines += [f"  Time Limit: {ai_config.get('time_limit', '?')}s"]

    lines += ['', dash, 'MOVE HISTORY', dash]
    for entry in log_data.get('move_history', []):
        lines.append(f'  {entry}')

    ai_logs = log_data.get('ai_move_logs', [])
    if ai_logs:
        lines += ['', dash, 'AI MOVE ANALYTICS', dash]
        total_nodes = 0
        total_prunes = 0
        total_time = 0.0
        max_depth_seen = 0
        for i, entry in enumerate(ai_logs, 1):
            lines += [f"Move {entry.get('move_num', i)}  {entry.get('move_text', '')}"]
            nodes  = entry.get('nodes', 0)
            prunes = entry.get('prunes', 0)
            depth  = entry.get('depth', 0)
            elapsed = entry.get('time', 0.0)
            lines += [f"  Nodes Expanded : {nodes:,}"]
            lines += [f"  Nodes Pruned   : {prunes:,}"]
            lines += [f"  Max Depth      : {depth}"]
            lines += [f"  Time Elapsed   : {elapsed:.3f}s"]
            total_nodes  += nodes
            total_prunes += prunes
            total_time   += elapsed
            max_depth_seen = max(max_depth_seen, depth)

        avg_time = total_time / len(ai_logs) if ai_logs else 0.0
        lines += ['', dash, 'CUMULATIVE AI STATISTICS', dash]
        lines += [f"  Total AI Moves       : {len(ai_logs)}"]
        lines += [f"  Total Nodes Expanded : {total_nodes:,}"]
        lines += [f"  Total Nodes Pruned   : {total_prunes:,}"]
        lines += [f"  Max Depth Reached    : {max_depth_seen}"]
        lines += [f"  Total Search Time    : {total_time:.3f}s"]
        lines += [f"  Avg Time per Move    : {avg_time:.3f}s"]

    lines += ['', dash, 'RESULT', dash]
    winner = log_data.get('winner')
    lines += [f"  Winner      : {winner if winner else 'N/A (incomplete)'}"]
    lines += [f"  Total Moves : {log_data.get('total_moves', 0)}"]
    lines += ['', sep]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    return filepath
