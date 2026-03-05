from GameBoard import GameBoard
from constants import WHITE, BLACK

class Checkers:
    """
    2 humans playing against each other, the bot will be added later
    """

    def __init__(self):
        self.game_board = GameBoard()
        self.move_number = 0  # to track how many moves happened
        self.current_player = WHITE  # the white player is the first one to start
    
    def switch_player(self):
        if self.current_player == WHITE:
            self.current_player = BLACK
        else:
            self.current_player = WHITE

    def get_move_location(self):  # get the move from any player
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
        """Check if the game is over (one player has no pieces left)."""
        white_count = 0
        black_count = 0
        for row in self.game_board.board:
            for cell in row:
                if cell.upper() == WHITE:
                    white_count += 1
                elif cell.upper() == BLACK:
                    black_count += 1
        
        if white_count == 0:
            print(f"Black wins after {self.move_number} moves")
            return True
        if black_count == 0:
            print(f"White wins after {self.move_number} moves")
            return True
        return False

        

    def play_human_turn(self):
        """Handle a single turn for the current human player."""
        print(f"\n{'='*50}")
        print(f"Player {self.current_player} Turn # {self.move_number+1}")

        self.game_board.display_board()

        # Keep asking for moves until a valid one is made
        move_successful = False
        while not move_successful:
            start_row, start_col, target_row, target_col = self.get_move_location()

            if self.game_board.make_move(start_row, start_col, target_row, target_col, self.current_player):
                self.move_number += 1
                print(f"Move {self.move_number} successful")
                move_successful = True
            else:
                print("Invalid move. Try again.")
        
    def play_game_two_players(self):
        """Main game loop for two human players."""
        while True:
            self.play_human_turn()
            if self.is_game_over():
                break
            self.switch_player()
    
        print("GAME OVER!")
        self.game_board.display_board()

if __name__ == "__main__":
    game = Checkers()
    game.play_game_two_players()