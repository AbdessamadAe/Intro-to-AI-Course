from GameBoard import GameBoard

class Checkers:
    """
    2 humans playing agaust each other, the bot will be added later
    """

    def __init__(self):
        self.gameBoard = GameBoard()
        self.moveNumber = 0 # to track how many moves happened 
        self.currentPlayer = 'W' #the white player is the first one to start

        #specified starting position by the Human
        self.StartingMoveLocationRow = 0
        self.StartingMoveLocationCol = 0

        #specified target position by the Human
        self.TargetingMoveLocationRow = 0
        self.TargetingMoveLocationCol = 0
    
    def SwitchPlayer(self):
        if self.currentPlayer == 'W':
            self.currentPlayer = 'B'
        else:
            self.currentPlayer = 'W'

    def GetMoveLocation (self): #get the move from any player

        while True:
            try:
                start_input = input(f'Player {self.currentPlayer} Move # {self.moveNumber+1} - starting location (row col): ').strip()
                row, col = map(int, start_input.split())
                self.StartingMoveLocationRow = row
                self.StartingMoveLocationCol = col
                break
                
            except ValueError:
                print("ERROR: Please enter two numbers: For example [6 1]")

        while True:
            try:
                target_input = input(f'Enter Target Location (row col): ').strip()
                row, col = map(int, target_input.split())
                self.TargetingMoveLocationRow  =  row
                self.TargetingMoveLocationCol = col
                break
            except ValueError:
                print("ERROR: Please enter two numbers: For example [6 1]")
       
    def IsGameOver (self):
        white_count = 0
        black_count = 0
        for row in self.gameBoard.board:
            for cell in row:
                if cell.upper() == 'W':
                    white_count +=1
                elif cell.upper() =='B':
                    black_count +=1
        
        if white_count ==0:
            print(f"Black wins after {self.moveNumber} moves")
            return True
        if black_count == 0:
            print(f"white wins after {self.moveNumber} moves")
            return True
        return False

        

    def PlayHumanTurn(self):
        print(f"\n{'='*50}")
        print(f"player {self.currentPlayer} Turn # {self.moveNumber+1}")

        self.gameBoard.DisplayBoard()

        self.GetMoveLocation()

        if self.gameBoard.MakeMove(self.StartingMoveLocationRow, self.StartingMoveLocationCol, self.TargetingMoveLocationRow, self.TargetingMoveLocationCol, self.currentPlayer):
            self.moveNumber+=1
            print(f"Move {self.moveNumber} successful")
        else:
            print("Try again")
            self.PlayHumanTurn()
        
    def PlayGameTwoPlayers(self):
        while True:
            self.PlayHumanTurn()
            if self.IsGameOver():
                break
            self.SwitchPlayer()
    
        print("GAME OVER!")
        self.gameBoard.DisplayBoard()

if __name__ == "__main__":
    game = Checkers()
    game.PlayGameTwoPlayers()   


    


#check final