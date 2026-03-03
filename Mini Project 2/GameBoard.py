
class GameBoard:
    def __init__(self):
        self.board = [] # creating the board
        for row_number in range(8):
            one_row= []
            for col_number in range(8):
                one_row.append('.') #creating a row that will be then integrated into the board
            
            self.board.append(one_row)

        self.SetupInitialBoard()

    def SetupInitialBoard(self):

        # WHITE peices (B) ABOVE
        self.board[0][1] = 'B'
        self.board[0][3] = 'B'
        self.board[0][5] = 'B'
        self.board[0][7] = 'B'

        self.board[1][0] = 'B'
        self.board[1][2] = 'B'
        self.board[1][4] = 'B'
        self.board[1][6] = 'B'
            
        self.board[2][1] = 'B'
        self.board[2][3] = 'B'
        self.board[2][5] = 'B'
        self.board[2][7] = 'B'

        #BLACK peices (B) LAST 3
        self.board[5][0] = 'W'
        self.board[5][2] = 'W'
        self.board[5][4] = 'W'
        self.board[5][6] = 'W'
            
        self.board[6][1] = 'W'
        self.board[6][3] = 'W'
        self.board[6][5] = 'W'
        self.board[6][7] = 'W'
        
        self.board[7][0] = 'W'
        self.board[7][2] = 'W'
        self.board[7][4] = 'W'
        self.board[7][6] = 'W'

    def DisplayBoard(self):
        print("  0 1 2 3 4 5 6 7") #prints teh number of the columns |
        for row in range(8):
            print(f"{row}", end="")  # prints through iterations the number of teh rows -- ex: 0 does not go to teh next line
            for col in range (8):
                print(f"{self.board[row][col]}", end="") #prints the content after all iteration B . B . B . B .
            print ()

    def IsValidMove(self, start_row, start_col, target_row, target_col, player):
        #checking the bounderies
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 
                0 <= target_row < 8 and 0 <= target_col < 8):
            return False
        
        #selecting the Own peice 
        piece = self.board[start_row][start_col]
        if piece not in [player, player.lower()]:  # 'W','w' or 'B','b'
            return False
            
        # target should be empty
        if self.board[target_row][target_col] != '.':
            return False
        
        #dioganal move ( 1 square only)
        row_diff = target_row - start_row
        col_diff = target_col - start_col
        
        if (abs(row_diff) != 1 or abs(col_diff) != 1) and (piece == 'W' or piece =='B'):
            return False
        
        #WHITE should move up ( to smaller numbers) unless it is a king
        if player == 'W':
            if row_diff > 0 and piece == 'W':  #  BLACK can't move down (not king) -- we go from 0 down to 7 that is why the difference is positive
                return False
            
        
        else: #BLACK should move down ( to bigger numbers) unless it is a king
            if row_diff < 0 and piece == 'B':  #BLACK can't move up (to smalle numbers)
                return False
        return True 

    def MakeMove(self, start_row, start_col, target_row, target_col, player):
        if not self.IsValidMove(start_row, start_col, target_row, target_col, player):
            print("Invalid Move")
            return False
        else:
            piece = self.board[start_row][start_col] 
            self.board[start_row][start_col] = '.' #removing the peice and placing
            self.board[target_row][target_col] = piece #placing the peice in teh target 

            #KING PROMOTIION IF IT REACHES THE OTHER END 
            if piece == 'W' and target_row == 0:
                self.board[target_row][target_col]='w' #SMALL w IS THE KING
            elif piece == 'B' and target_row == 7:
                self.board[target_row][target_col]='b' #SMALL b IS THE KING
            
            print(f"SUCCESS: ({start_row},{start_col}) -> ({target_row},{target_col})")
            self.DisplayBoard()
            return True





        
            

