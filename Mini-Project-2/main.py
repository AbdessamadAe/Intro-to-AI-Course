"""
Checkers Game - Main Entry Point

Run this file to play Checkers with flexible interface and game mode options:

Interface Options:
- Console: Text-based interface
- GUI: Graphical interface

Game Modes:
- Human vs Human: Two players take turns
- Human vs AI: Play against AI with configurable search algorithms

The AI can use three search strategies:
- Minimax: Basic minimax search
- AlphaBeta: Alpha-beta pruning for efficiency
- AlphaBetaOrdering: Alpha-beta with move ordering (recommended)
"""

from PlayingTheGame import Checkers

def get_ai_configuration():
    """Prompt user for AI configuration settings."""
    print("\n" + "="*60)
    print("AI CONFIGURATION")
    print("="*60)
    print("\nSearch Strategies:")
    print("1. Minimax (basic)")
    print("2. Minimax + AlphaBeta Pruning (efficient)")
    print("3. Minimax + AlphaBeta with Ordering (recommended)")
    
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
    
    return strategy, depth, time_limit

def main():
    print("\n" + "="*60)
    print("WELCOME TO CHECKERS!")
    print("="*60)
    
    # Step 1: Choose Interface
    print("\nSelect Interface:")
    print("1. Console (Text-based)")
    print("2. GUI (Graphical)")
    
    while True:
        try:
            interface = input("\nSelect interface (1-2): ").strip()
            if interface in ['1', '2']:
                break
            print("Invalid input. Please enter 1 or 2.")
        except (ValueError, EOFError):
            print("Invalid input. Please enter 1 or 2.")
    
    # Step 2: Choose Game Mode
    print("\nSelect Game Mode:")
    print("1. Human vs Human")
    print("2. Human (WHITE) vs AI (BLACK)")
    
    while True:
        try:
            game_mode = input("\nSelect game mode (1-2): ").strip()
            if game_mode in ['1', '2']:
                break
            print("Invalid input. Please enter 1 or 2.")
        except (ValueError, EOFError):
            print("Invalid input. Please enter 1 or 2.")
    
    # Step 3: Configure AI if needed
    ai_config = None
    if game_mode == '2':
        ai_config = get_ai_configuration()
    
    # Step 4: Launch appropriate mode
    if interface == '2':  # GUI
        print("\nLaunching GUI...")
        try:
            from GUI.checkersGui import CheckerGUI
            if game_mode == '1':
                print("Starting Human vs Human GUI...")
                app = CheckerGUI(ai_enabled=False)
            else:
                strategy, depth, time_limit = ai_config
                print(f"Starting Human vs AI GUI (Strategy: {strategy}, Depth: {depth}, Time: {time_limit}s)...")
                app = CheckerGUI(ai_enabled=True, ai_strategy=strategy, ai_depth=depth, ai_time_limit=time_limit)
        except ImportError as e:
            error_msg = str(e)
            print("\n" + "="*60)
            print("⚠️  GUI NOT AVAILABLE")
            print("="*60)
            if 'tkinter' in error_msg or '_tkinter' in error_msg or 'libtk' in error_msg:
                print("\nThe GUI requires tkinter, which is not installed or configured.")
                print("\nTo install tkinter on Ubuntu/Debian:")
                print("  sudo apt-get install python3-tk")
                print("\nTo install tkinter on Fedora/Red Hat:")
                print("  sudo dnf install python3-tkinter")
                print("\nTo install tkinter on Arch:")
                print("  sudo pacman -S tk")
            else:
                print(f"\nImport error: {e}")
            print("\nPlease use console mode instead.")
            print("="*60)
        except Exception as e:
            print(f"\n⚠️  Error launching GUI: {e}")
            print("Please use console mode instead.")
    else:  # Console
        game = Checkers()
        if game_mode == '1':
            print("\nStarting Human vs Human (Console)...")
            game.play_game_two_players()
        else:
            strategy, depth, time_limit = ai_config
            print(f"\nStarting Human vs AI (Console)...")
            game.play_game_human_vs_ai(strategy, depth, time_limit)

if __name__ == "__main__":
    main()
