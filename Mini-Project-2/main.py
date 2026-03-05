from board import GameBoard
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
        """Handle a single turn for the current human player.
        
        Handles multi-jump sequences: if a piece jumps and can jump again,
        the player must continue jumping with the same piece.
        """
        print(f"\n{'='*50}")
        print(f"Player {self.current_player} Turn # {self.move_number+1}")

        self.game_board.display_board()

        # Check if jumps are available (mandatory jump rule)
        jumps_available = self.game_board.has_jump(self.current_player)
        if jumps_available:
            print(f"⚠ JUMP AVAILABLE! You must jump.")

        # Keep asking for moves until a valid one is made
        move_successful = False
        landing_row = None
        landing_col = None
        
        while not move_successful:
            start_row, start_col, target_row, target_col = self.get_move_location()

            # Check if attempting a simple move when jumps are mandatory
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
        
        # Handle multi-jump sequences
        if result['was_jump']:
            # If promoted to king, turn ends (standard checkers rule)
            if result['promoted']:
                print("Promoted to KING! Turn ends.")
                self.move_number += 1
                return
            
            # Check for additional jumps from landing position
            while self.game_board.has_jump_from_position(landing_row, landing_col, self.current_player):
                print("\n" + "="*50)
                print(f"⚠ ADDITIONAL JUMP AVAILABLE! You must continue jumping.")
                self.game_board.display_board()
                
                # Get next jump (must start from landing position)
                jump_made = False
                while not jump_made:
                    start_row, start_col, target_row, target_col = self.get_move_location()
                    
                    # Validate that move starts from the landing position
                    if start_row != landing_row or start_col != landing_col:
                        print(f"Invalid: You must continue jumping with the piece at ({landing_row}, {landing_col})!")
                        continue
                    
                    # Validate that it's a jump (distance = 2)
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
                
                # If promoted during multi-jump, turn ends
                if result['promoted']:
                    print("Promoted to KING! Turn ends.")
                    break
        
        self.move_number += 1
        print(f"\nTurn complete! Total moves: {self.move_number}")
        
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