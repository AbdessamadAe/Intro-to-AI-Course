import GameBoard

class playingTheGame:
    """
    handles complete workflow between the white (human) and  the black (bot)
    """

    def __init__(self):
        self.gameBoard = GameBoard()
        self.moveNumber = 0 # to track how many moves happened 

        #specified starting potion by the Human
        self.MoveStartingLocationRow = 0
        self.MoveStartingLocationCol = 0

        #specified target potion by the Human
        self.TargetingMoveLocationRow = 0
        self.TargetingMoveLocationCol = 0

    def getStartingMoveLocation (self): #from the human whenerver it is his turn
