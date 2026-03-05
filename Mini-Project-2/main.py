"""
Checkers Game - Main Entry Point

Run this file to play Checkers:
- Mode 1: Two human players
- Mode 2: Human (WHITE) vs AI (BLACK)

The AI can use three search strategies:
- Minimax: Basic minimax search
- AlphaBeta: Alpha-beta pruning for efficiency
- AlphaBetaOrdering: Alpha-beta with move ordering (recommended)
"""

from PlayingTheGame import Checkers

def main():
    print("\n" + "="*60)
    print("WELCOME TO CHECKERS!")
    print("="*60)
    print("\nGame Modes:")
    print("1. Two Human Players")
    print("2. Human (WHITE) vs AI (BLACK)")
    
    while True:
        try:
            mode = input("\nSelect game mode (1 or 2): ").strip()
            if mode in ['1', '2']:
                break
            print("Invalid input. Please enter 1 or 2.")
        except (ValueError, EOFError):
            print("Invalid input. Please enter 1 or 2.")
    
    game = Checkers()
    
    if mode == '1':
        print("\nStarting Two-Player Game...")
        game.play_game_two_players()
    else:
        print("\n" + "="*60)
        print("AI CONFIGURATION")
        print("="*60)
        print("\nSearch Strategies:")
        print("1. Minimax (basic)")
        print("2. AlphaBeta (efficient)")
        print("3. AlphaBetaOrdering (recommended)")
        
        while True:
            try:
                strategy_choice = input("\nSelect strategy (1-3, default=3): ").strip()
                if strategy_choice == '' or strategy_choice == '3':
                    strategy = 'AlphaBetaOrdering'
                    break
                elif strategy_choice == '1':
                    strategy = 'Minimax'
                    break
                elif strategy_choice == '2':
                    strategy = 'AlphaBeta'
                    break
                print("Invalid input. Please enter 1, 2, or 3.")
            except (ValueError, EOFError):
                strategy = 'AlphaBetaOrdering'
                break
        
        while True:
            try:
                depth_input = input("Search depth (5-9, default=7): ").strip()
                if depth_input == '':
                    depth = 7
                    break
                depth = int(depth_input)
                if 5 <= depth <= 9:
                    break
                print("Depth must be between 5 and 9.")
            except (ValueError, EOFError):
                depth = 7
                break
        
        while True:
            try:
                time_input = input("Time limit in seconds (1-3, default=3): ").strip()
                if time_input == '':
                    time_limit = 3.0
                    break
                time_limit = float(time_input)
                if 1.0 <= time_limit <= 3.0:
                    break
                print("Time limit must be between 1 and 3 seconds.")
            except (ValueError, EOFError):
                time_limit = 3.0
                break
        
        print("\nStarting Human vs AI Game...")
        game.play_game_human_vs_ai(strategy, depth, time_limit)

if __name__ == "__main__":
    main()
