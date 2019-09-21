import copy

class game:
    def __init__(self, board, turn, row, col, win):
        ''' Initializes the game by setting the board, rows, columns, 
        number of black and white pieces and how the game is won '''
        self._board = board
        self._row = row 
        self._column = col
        self._black = 0
        self._white = 0
        self._win = win
        self._turn = turn
    
    def _moves(self,x, y, deltax, deltay, check) -> bool:
        ''' Takes in three parameters x the row, y the column and check if you want to flip tiles.
        Checks if you can make a move in the upward direction and returns a boolean. 
        If check and opp is True then it flips the tiles '''
        # make it return new_x and the bool as a tuple
        new_x = x + deltax
        new_y = y + deltay
        opp = False
        see = False
        while(new_x >= 0 and new_x < self._row and new_y < self._column and new_y >= 0):
            if self._board[new_x][new_y] == 0:
                return False
            elif self._board[new_x][new_y] == self._turn:
                see = True
                if opp and check == True:
                    if deltax != 0 and deltay == 0:
                        while(x != new_x):
                            self._board[x][y] = self._turn
                            x += deltax
                    elif deltax == 0 and deltay != 0:
                        while(y != new_y):
                            self._board[x][y] = self._turn
                            y += deltay
                    else:
                        while(x != new_x and y != new_y):
                            self._board[x][y] = self._turn
                            x += deltax
                            y += deltay
                # might just want to return opp only and do the above inside of go then delete it 
                return opp
            elif deltax != 0:
                if deltay == 0:
                    if self._board[new_x][y] == game._opposite_turn(self,self._turn):
                        opp = True
                        new_x += deltax
                else:
                    if self._board[new_x][new_y] == game._opposite_turn(self,self._turn):
                        opp = True
                        new_x += deltax
                        new_y += deltay
            elif deltax == 0:
                if deltay != 0:
                    if self._board[x][new_y] == game._opposite_turn(self,self._turn):
                        opp = True
                        new_y += deltay
        #return only opp 
        return opp and see
    
    def lets_see(self) -> bool:
        ''' Sees if there's any valid moves for whichever player turn it is '''
        see = set()
        check = False
        for row_1 in range(len(self._board)):
            for col_1 in range(len(self._board[row_1])):
                if self._board[row_1][col_1] in [1,2] :
                    continue
                s = self.go(row_1, col_1, check)
                see = see | s
        if True not in see:
            self._switch_turn(self._turn)
            return False
        if True in see:
            return True
    
    def _any_moves(self) -> bool:
        ''' Sees if any player can not make a move '''
        save_turn = self._turn
        if self.lets_see() == False:
            self._switch_turn(save_turn)
            if self.lets_see() == False:
                #self._turn = save_turn
                return True
        self._turn = save_turn
        return False
    
    def _switch_turn(self,turn):
        self._turn = self._opposite_turn(turn)
    
    def skip_turn(self) -> str:
        ''' Returns which turn was skipped '''
        if self._turn == 1:
            return 'White'
        else:
            return 'Black'
        
    def go(self, row, col,see):
        ''' Takes 2 parameters the row and the column desired of where the player wants to place a piece.
        Checks all directions and sees if the user can place it there if so then it places the piece there
        and the tiles flip. It switches turns if the player can place a piece somewhere. '''
        check = set()
        moves = []
        move = False
        if col - 1 >= 0 and self._board[row][col -1] == self._opposite_turn(self._turn):
            move = self._moves(row, col, 0, -1, see)
            check.add(move)
            moves.append((0,-1))
        if col + 1 < self._column and self._board[row][col + 1] == self._opposite_turn(self._turn):
            move = self._moves(row, col, 0, 1, see)
            check.add(move)
            moves.append((0,1))
        if row - 1 >= 0 and self._board[row - 1][col] == self._opposite_turn(self._turn):
            move = self._moves(row, col, -1, 0, see)
            check.add(move)
            moves.append((-1,0))
        if row + 1 < self._row and self._board[row+1][col] == self._opposite_turn(self._turn):
            move = self._moves(row, col,1, 0, see)
            check.add(move)
            moves.append((1,0))
        if row - 1 >= 0 and col - 1 >= 0 and self._board[row - 1][col -1] == self._opposite_turn(self._turn):
            move = self._moves(row, col, -1, -1, see)
            check.add(move)
            moves.append((-1,-1))
        if row + 1 < self._row and col - 1 >= 0 and self._board[row+1][col-1] == self._opposite_turn(self._turn):
            move = self._moves(row, col, 1, -1, see)
            check.add(move)
            moves.append((1,-1))
        if row - 1 >= 0 and col + 1 < self._column and self._board[row -1][col+1] == self._opposite_turn(self._turn):
            move = self._moves(row, col, -1, 1, see)
            check.add(move)
            moves.append((-1,1))
        if row + 1 < self._row and col + 1 < self._column and self._board[row +1][col+1] == self._opposite_turn(self._turn):
            move = self._moves(row, col, 1, 1, see)
            check.add(move)
            moves.append((1,1))
        if see == True and True in check:
            self._turn = game._opposite_turn(self,self._turn)
        if (see == False):
            return check
        else:
            return None
                
    def _opposite_turn(self, turn:int) -> int:
        ''' Returns the opposite turn'''
        if turn == 1:
            return 2
        else:
            return 1

    def get_board(self) -> list:
        ''' Returns the gameboard '''
        return self._board
    
    def get_turn(self) -> int:
        ''' Returns the current turn '''
        return self._turn
    
    def get_row(self) -> int:
        ''' Returns the amount of rows '''
        return self._row
    
    def get_column(self) -> int:
        ''' Returns the amount of columns '''
        return self._column
    
    def get_win(self) -> str:
        ''' Returns how the game is won '''
        return self._win
    
    def get_black(self) -> int:
        ''' Returns the amount of black discs '''
        self._count()
        return self._black
    
    def get_white(self) -> int:
        ''' Returns the amount of white discs '''
        self._count()
        return self._white
        
    def check_if_empty(self, col:int, row:int) -> bool:
        ''' Takes in two parameters the row and column number of the desired move. Returns True or False if the user
        can put a piece there. '''
        if self._board[col][row] == 1 or self._board[col][row] == 2:
            return False
        else: 
            return True
        
    def _count(self) -> None:
        ''' Counts up the number of black and white pieces '''
        b_num = 0
        w_num = 0
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] == 1:
                    b_num += 1
                elif self._board[i][j] == 2:
                    w_num += 1
        self._black = b_num
        self._white = w_num
        return None

    def see_winner(self) -> str:
        ''' Sees if there's a winner if not returns None '''
        if self._any_moves() == True:      
            self._count()
            if self._win == '>':
                if self._black > self._white:
                    return 'WINNER: BLACK'
                elif self._black < self._white:
                    return 'WINNER: WHITE'
                else:
                    return 'WINNER: NONE'
            elif self._win == '<':
                if self._black > self._white:
                    return 'WINNER: WHITE'
                elif self._black < self._white:
                    return 'WINNER: BLACK'
                else:
                    return 'WINNER: NONE'
        return None
    
    def _clone(self):
        return copy.deepcopy(self)
    
class AI(game):
    def __init__(self, gameState):
        self._game = gameState
        super().__init__(self._game._board, self._game._turn, self._game._row, self._game._column, self._game._win)
        self._currTurn = True
    
    def _possibleMoves(self,clone) -> [(int,int)]:
        ''' Gets the possible moves of the current clone and stores them in a list of tuples '''
        moves = []
        for row in range(len(clone._board)):
            for col in range(len(clone._board[row])):
                if ( True in clone.go(row, col, False) ):
                    moves.append((row,col))  
        return moves
    
    def chooseMove(self) -> (int,int):
        ''' Finds the best move for the AI and return it as a tuple '''
        clone = self._game._clone()
        moves = self._possibleMoves(clone)
        self._currTurn = self._seeTurn(clone)
        maxValue = -1000
        index = 0
        for move in range(len(moves)):
            tempClone = clone._clone()
            tempClone.go(moves[move][0], moves[move][1], True)
            tempSearch = self._search(tempClone, 2)
            tempMax = max(tempSearch,maxValue)
            if tempMax == tempSearch:
                maxValue = tempMax
                index = move
            del tempClone
        del clone
        return moves[index]
    
    def _search(self,clone,depth) -> int:
        ''' Uses a Heuristic search algorithm to find the best move from the game tree '''
        if depth == 0:
            newClone = clone._clone()
            total = self._evaluation(newClone)
            del newClone
            return total
        if self._currTurn == self._seeTurn(clone):
            newClone = clone._clone()
            moves = self._possibleMoves(newClone)
            tempMax = -1000
            for move in range(len(moves)):
                tempClone = clone._clone()
                tempClone.go(moves[move][0],moves[move][1],True)
                tempMax = max(tempMax,self._search(tempClone, depth-1))
                del tempClone
            return tempMax
        else:
            newClone = clone._clone()
            moves = self._possibleMoves(newClone)
            tempMin = 1000
            for move in range(len(moves)):
                tempClone = clone._clone()
                tempClone.go(moves[move][0],moves[move][1],True)
                tempMin = min(tempMin,self._search(tempClone, depth-1))
                del tempClone
            return tempMin

    def _evaluation(self,clone) -> int:
        ''' Evaluates the current difference of the scores '''
        if(self._currTurn):
            return clone.get_black() - clone.get_white()
        return clone.get_white() - clone.get_black()
        
    def _seeTurn(self,clone):
        ''' Returns true if the turn is black and false if white '''
        if clone.get_turn() == 1:
            return True
        return False
    