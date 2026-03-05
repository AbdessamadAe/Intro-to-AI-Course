"""
Checkers Game - Main Entry Point

Run this file to play Checkers:
- Currently supports two human players
- AI opponent will be added later
"""

from PlayingTheGame import Checkers

if __name__ == "__main__":
    game = Checkers()
    game.play_game_two_players()