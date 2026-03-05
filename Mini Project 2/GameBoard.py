
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

        # WHITE pieces (B) ABOVE
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

        #BLACK pieces (B) LAST 3
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
        #print("  0 1 2 3 4 5 6 7") #prints teh number of the columns |
        for row in range(8):
            #print(f"{row}", end="")  # prints through iterations the number of teh rows -- ex: 0 does not go to teh next line
            for col in range (8):
                print(f"{self.board[row][col]}", end="") #prints the content after all iteration B . B . B . B .
            print ()   
        print()

    def IsValidMove(self, start_row, start_col, target_row, target_col, player):
        #checking the bounderies
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 
                0 <= target_row < 8 and 0 <= target_col < 8):
            return False
        
        #selecting the Own peice 
        piece = self.board[start_row][start_col]
        if piece not in [player, player.lower()]:  # 'W','w' or 'B','b'
            return False

        row_diff = target_row - start_row
        col_diff = target_col - start_col

        #WHITE should move up ( to smaller numbers) unless it is a king
        if player == 'W':
            if row_diff > 0 and piece == 'W':  #  BLACK can't move down (not king) -- we go from 0 down to 7 that is why the difference is positive
                return False
            
        else: #BLACK should move down ( to bigger numbers) unless it is a king
            if row_diff < 0 and piece == 'B':  #BLACK can't move up (to smalle numbers)
                return False            

        #dioganal move, even king move the same number
     
        if abs(row_diff) not in (1,2) or abs(col_diff) not in  (1,2) or abs(row_diff) != abs(col_diff): #1 simple / 2 jump
            return False
        
        #simple move
        if abs(row_diff) == 1:
            if self.board[target_row][target_col] != '.': #target must be empty
                return False
            return True
        
        #when we having a jump
        if abs(row_diff) == 2: 
            if self.board[target_row][target_col] != '.': #target empty for landing
                return False
            #enemy in the middle
            mid_row = (start_row + target_row) // 2
            mid_col = (start_col + target_col) // 2
            mid_piece = self.board[mid_row][mid_col]
            if mid_piece == '.' or mid_piece.upper() == player.upper(): #must be opponent 
                return False
            return True

    def HasJump (self,player): # checking if it has any opponent piece to jump over and eat ------------ can be in the ui 
        for row in range(8):
            for col in range(8):
                if self.board[row][col] in [player, player.lower()]: #the players piece
                    for jump_row, jump_col in [(-2,-2), (-2,2), (2,-2),(2,2)]:
                        new_row = row + jump_row
                        new_col = col + jump_col

                        if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] == '.':
                            #check for anemy in the middle 
                            middle_row = (row + new_row)//2
                            middle_col = (col + new_col)//2
                            enemy_there = self.board[middle_row][middle_col]
                            
                            if enemy_there != '.'and enemy_there.upper() != player.upper():
                                return True
        return False
                            

    def MakeMove(self, start_row, start_col, target_row, target_col, player):
        if not self.IsValidMove(start_row, start_col, target_row, target_col, player):
            print("Invalid Move")
            return False
        
          
        piece = self.board[start_row][start_col] 

        self.board[start_row][start_col] = '.'
        self.board[target_row][target_col] = piece

        #handle jump
        if abs(target_row - start_row) == 2:
            mid_row = (start_row + target_row) // 2
            mid_col = (start_col + target_col) // 2
            self.board[mid_row][mid_col] = '.'
                
                

        #KING PROMOTIION IF IT REACHES THE OTHER END 
        if piece == 'W' and target_row == 0:
            self.board[target_row][target_col]='w' #SMALL w IS THE KING
        elif piece == 'B' and target_row == 7:
            self.board[target_row][target_col]='b' #SMALL b IS THE KING
            
        print(f"SUCCESS: ({start_row},{start_col}) -> ({target_row},{target_col})")
        self.DisplayBoard()
        return True
        
# 2 moves - eat
#

gameboard = GameBoard()
gameboard.DisplayBoard()





        
            

