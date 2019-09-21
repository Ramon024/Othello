import tkinter
import othello_logic_gui
import point

DEFAULT_FONT = ('Helvetica', 20)

class start:
    def __init__(self):
        self._root_window = tkinter.Tk()
        self._root_window.title('PICK A GAME MODE')
        mainframe = tkinter.Frame(self._root_window)
        mainframe.grid(column=0,row=0, sticky=(tkinter.N,tkinter.W,tkinter.E,tkinter.S) )
        mainframe.columnconfigure(0, weight = 1)
        mainframe.rowconfigure(0, weight = 1)
        mainframe.pack()
        self._mode_option = tkinter.StringVar(self._root_window)
        turn = ['2 Player', 'CPU']
        self._mode_option.set('2 Player')
        popup_turn = tkinter.OptionMenu(mainframe, self._mode_option, *turn)
        tkinter.Label(mainframe, text='Choose a game mode ').grid(row = 1, column = 1)
        popup_turn.grid(row = 2, column =1)
        ok_button = tkinter.Button(master = mainframe, text = 'Go to game options', font = DEFAULT_FONT, command = self._on_ok_button)
        ok_button.grid(row = 3, column = 1)
        cancel_button = tkinter.Button(master = mainframe, text = 'Cancel', font = DEFAULT_FONT, command = self._on_cancel_button)
        cancel_button.grid(row = 4, column = 1)
        
    def _on_ok_button(self):
        mode = self._mode_option.get()
        self._root_window.destroy()
        game_options(mode).run()
        
    def _on_cancel_button(self):
        ''' If pressed on cancel the the program will destroy this window '''
        self._root_window.destroy()
        
    def run(self) -> None:
        ''' Runs the game options.'''
        self._root_window.mainloop()
        
class game_options:
    def __init__(self, mode):
        ''' Initializes the window. Sets up an option window and asks the user the how they want to play the game '''
        self._mode = mode
        self._root_window = tkinter.Tk()
        self._root_window.title('OTHELLO GAME OPTIONS')
        mainframe = tkinter.Frame(self._root_window)
        mainframe.grid(column=0,row=0, sticky=(tkinter.N,tkinter.W,tkinter.E,tkinter.S) )
        mainframe.columnconfigure(0, weight = 1)
        mainframe.rowconfigure(0, weight = 1)
        mainframe.pack()
        self._turn_option = tkinter.StringVar(self._root_window)
        turn = ['Black', 'White']
        self._turn_option.set('Black')
        popup_turn = tkinter.OptionMenu(mainframe, self._turn_option, *turn)
        tkinter.Label(mainframe, text='Whose turn is it? ').grid(row = 1, column = 1)
        popup_turn.grid(row = 2, column =1)
        self._win_option = tkinter.StringVar(self._root_window)
        won = ['More Discs', 'Less Discs']
        self._win_option.set('More Discs')
        popupWon = tkinter.OptionMenu(mainframe, self._win_option, *won)
        tkinter.Label(mainframe, text='How will the game be won ').grid(row = 1, column = 2)
        popupWon.grid(row = 2, column =2)
        self._rows_option = tkinter.StringVar(self._root_window)
        rows = ['4', '6', '8', '10', '12', '14', '16']
        self._rows_option.set('4')
        popupRow = tkinter.OptionMenu(mainframe, self._rows_option, *rows)
        tkinter.Label(mainframe, text='How many rows? ').grid(row = 3, column = 1)
        popupRow.grid(row = 4, column =1)
        self._cols_option = tkinter.StringVar(self._root_window)
        cols = ['4', '6', '8', '10', '12', '14', '16']
        self._cols_option.set('4')
        popupCol = tkinter.OptionMenu(mainframe, self._cols_option, *cols)
        tkinter.Label(mainframe, text='How many columns? ').grid(row = 3, column = 2)
        popupCol.grid(row = 4, column =2)
        ok_button = tkinter.Button(master = mainframe, text = 'Set up board', font = DEFAULT_FONT, command = self._on_ok_button)
        ok_button.grid(row = 5, column = 1)
        cancel_button = tkinter.Button(master = mainframe, text = 'Cancel', font = DEFAULT_FONT, command = self._on_cancel_button)
        cancel_button.grid(row = 5, column = 2)

    def _on_ok_button(self):
        ''' If the user presses ok then the program will then proceed to destroy this window and 
        open up another window to set up the pieces. '''
        player = self._turn_option.get()
        win = self._win_option.get()
        rows = self._rows_option.get()
        cols = self._cols_option.get()
        if player == 'Black':
            player = 1
        else:
            player = 2
        if win == 'More Discs':
            winnner = '>'
        else:
            winnner = '<'
        self._root_window.destroy()
        setup_gameboard(player, winnner, int(rows), int(cols), self._mode).run()
    
    def _on_cancel_button(self):
        ''' If pressed on cancel the the program will destroy this window '''
        self._root_window.destroy()
        
    def run(self) -> None:
        ''' Runs the game options.'''
        self._root_window.mainloop()
        
class setup_gameboard:
    def __init__(self, player, win, rows, cols, mode):
        ''' Initializes the window and handles any mouse clicks and resizing '''
        self._root_window = tkinter.Tk()
        self.board = self._make_board(rows, cols)
        self._mode = mode
        self._game = othello_logic_gui.game(self.board, player, rows, cols, win)
        self._root_window.grid()
        self._root_window.title('SETUP BOARD')
        self._canvas = tkinter.Canvas(master = self._root_window, width = 594, height = 594, background = '#03af01')
        self._canvas.grid(row = 1, column = 0, padx =20, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._draw_lines()
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._mouse_clicked)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._label_black = tkinter.Label(master = self._root_window, text = 'Black: 0', font = DEFAULT_FONT)
        self._label_black.grid(row = 0, column = 0, sticky = tkinter.W)
        self._label_white = tkinter.Label(master = self._root_window, text = 'White: 0', font = DEFAULT_FONT)
        self._label_white.grid(row = 0, column = 0, sticky = tkinter.E)
        self._label_place = tkinter.Label(master = self._root_window, text = "Black's Turn to place pieces", font = DEFAULT_FONT)
        self._label_place.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.S)
        self._switch_button = tkinter.Button(master = self._root_window, text = 'Switch To White', font = DEFAULT_FONT, command = self._on_switch_button)
        self._switch_button.grid(row = 2, column = 0, sticky = tkinter.W)
        ok_button = tkinter.Button(master = self._root_window, text = 'Start Game', font = DEFAULT_FONT, command = self._on_start_button)
        ok_button.grid(row = 2, column = 0, sticky = tkinter.E)
        self._turn = 1
        
    def _draw_lines(self):
        ''' Draws the initial board '''
        canvas_width = self._canvas.winfo_reqwidth()
        canvas_height = self._canvas.winfo_reqheight()
        deltax = canvas_width / othello_logic_gui.game.get_column(self._game) 
        deltay = canvas_height / othello_logic_gui.game.get_row(self._game)
        for x in range(othello_logic_gui.game.get_row(self._game)):
            self._canvas.create_line(0, x*deltax, canvas_width, x*deltax,fill = 'black')
        for y in range(othello_logic_gui.game.get_column(self._game)):
            self._canvas.create_line(y*deltay, 0, y*deltay, canvas_height,fill = 'black')
            
    def _make_board(self,rows, cols) -> list:
        ''' Makes the a blank board full of zeros. '''
        l = []
        for _ in range(rows):
            l1 = []
            for _ in range(cols):
                l1.append(0)
            l.append(l1)
        return l
        
    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''' Redraws the board if resized '''
        self._redraw_board()
        
    def _redraw_board(self) -> None:
        ''' Redraws the board if a disc is placed or if resized '''
        self._canvas.delete(tkinter.ALL)
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        deltax = canvas_width / othello_logic_gui.game.get_column(self._game)
        deltay = canvas_height / othello_logic_gui.game.get_row(self._game)
        for x in range(othello_logic_gui.game.get_column(self._game)):
            self._canvas.create_line(x*deltax, 0, x*deltax, canvas_height,fill = 'black')
        for y in range(othello_logic_gui.game.get_row(self._game)):
            self._canvas.create_line(0, y*deltay, canvas_width, y*deltay,fill = 'black')
        for row in range(len(othello_logic_gui.game.get_board(self._game))):
            for col in range(len(othello_logic_gui.game.get_board(self._game)[row])):
                if othello_logic_gui.game.get_board(self._game)[row][col] == 1:
                    x1 = col * deltax
                    x2 = (col + 1) * deltax
                    y1 = row * deltay
                    y2 = (row + 1) * deltay
                    self._canvas.create_oval(x1, y1, x2, y2, fill = 'black')
                elif othello_logic_gui.game.get_board(self._game)[row][col] == 2:
                    x1 = col * deltax
                    x2 = (col + 1) * deltax
                    y1 = row * deltay
                    y2 = (row + 1) * deltay
                    self._canvas.create_oval(x1, y1, x2, y2, fill = 'white')
    
    def _on_switch_button(self):
        ''' Switches the turn to white.'''
        if self._turn == 1:
            self._turn = 2
            self._label_place['text'] = "White's Turn to place pieces"
            self._switch_button['text'] = 'Switch To Black'
        else:
            self._turn = 1
            self._label_place['text'] = "Blacks's Turn to place pieces"
            self._switch_button['text'] = 'Switch To White'
    
    def _on_start_button(self):
        ''' Destroys the game options window and opens up the window to setup the board. ''' 
        self._root_window.destroy()
        if othello_logic_gui.game.get_turn(self._game) == 1:
            players = "Black's"
        else:
            players = "White's"
        if othello_logic_gui.game.get_win(self._game) == '>':
            winner = 'The player with the most amount of discs wins'
        else:
            winner = 'The player with the least amount of discs wins'
        #if self._mode == "2 Player":
        twoPlayerOthello(str(othello_logic_gui.game.get_black(self._game)), str(othello_logic_gui.game.get_white(self._game)), 
                         players, winner, self._game, self._mode).run()
        #else:
            #CPUothello(str(othello_logic_gui.game.get_black(self._game)), str(othello_logic_gui.game.get_white(self._game)), players, winner, self._game).run()
        
    def _mouse_clicked(self, event:tkinter.Event):  
        ''' Sees if the cell where the user clicked is empty and if so places a disc there '''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        click_point = point.Point(event.x, event.y, width, height, othello_logic_gui.game.get_row(self._game), othello_logic_gui.game.get_column(self._game))
        see_row = click_point.check_row()
        see_column = click_point.check_column()
        if othello_logic_gui.game.check_if_empty(self._game, see_row, see_column) == True:
            othello_logic_gui.game.get_board(self._game)[see_row][see_column] = self._turn
            self._update_scoreboard()
            self._redraw_board()
        elif othello_logic_gui.game.get_board(self._game)[see_row][see_column] == self._turn:
            othello_logic_gui.game.get_board(self._game)[see_row][see_column] = 0
            self._update_scoreboard()
            self._redraw_board()
            
    def _update_scoreboard(self):
        ''' Updates the scoreboard '''
        self._label_black['text'] = 'Black: ' + str(othello_logic_gui.game.get_black(self._game))
        self._label_white['text'] = 'White: ' + str(othello_logic_gui.game.get_white(self._game))
            
    def run(self) -> None:
        ''' Runs the setup_gameboard class '''
        self._root_window.mainloop()
        


class CPUothello:
    def __init__(self,b_num, w_num, players, winner, game):
        pass
        
class twoPlayerOthello:
    def __init__(self, b_num, w_num, players, winner, game, mode):
        ''' Initializes the window, plays the game and handles any resiszing. '''
        self._game = game
        self._mode = mode
        self.num = 1
        self._root_window = tkinter.Tk()
        self._root_window.grid()
        self._root_window.title('FULL OTHELLO')
        self._canvas = tkinter.Canvas(master = self._root_window, width = 600, height = 600, background = '#03af01')
        self._canvas.grid(row = 1, column = 0, padx =20, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._start_board()
        self._label_black = tkinter.Label(master = self._root_window, text = 'Black: ' + b_num, font = DEFAULT_FONT)
        self._label_black.grid(row = 0, column = 0, sticky = tkinter.W)
        self._label_white = tkinter.Label(master = self._root_window, text = 'White: ' + w_num, font = DEFAULT_FONT)
        self._label_white.grid(row = 0, column = 0, sticky = tkinter.E)
        self._label_turn = tkinter.Label(master = self._root_window, text = players + ' Turn', font = DEFAULT_FONT)
        self._label_turn.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.S)
        self._how_to_win = tkinter.Label(master = self._root_window, text = winner, font = DEFAULT_FONT)
        self._how_to_win.grid(row = 2, column = 0, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._mouse_clicked)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        
    def _start_board(self):
        ''' Draws the initial starting board '''
        canvas_width = self._canvas.winfo_reqwidth()
        canvas_height = self._canvas.winfo_reqheight()
        deltax = canvas_width / othello_logic_gui.game.get_column(self._game) 
        deltay = canvas_height / othello_logic_gui.game.get_row(self._game)
        for x in range(othello_logic_gui.game.get_row(self._game)):
            self._canvas.create_line(0, x*deltax, canvas_width, x*deltax,fill = 'black')
        for y in range(othello_logic_gui.game.get_column(self._game)):
            self._canvas.create_line(y*deltay, 0, y*deltay, canvas_height,fill = 'black')
        for row in range(len(othello_logic_gui.game.get_board(self._game))):
            for col in range(len(othello_logic_gui.game.get_board(self._game)[row])):
                if othello_logic_gui.game.get_board(self._game)[row][col] == 1:
                    x1 = col * deltax
                    x2 = (col + 1) * deltax
                    y1 = row * deltay
                    y2 = (row + 1) * deltay
                    self._canvas.create_oval(x1, y1, x2, y2, fill = 'black')
                elif othello_logic_gui.game.get_board(self._game)[row][col] == 2:
                    x1 = col * deltax
                    x2 = (col + 1) * deltax
                    y1 = row * deltay
                    y2 = (row + 1) * deltay
                    self._canvas.create_oval(x1, y1, x2, y2, fill = 'white')
                
    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        ''' Handles any resizing by redrawing the board '''
        self._redraw_board()
    
    def _redraw_board(self) -> None:
        ''' Redraws the board if the canvas was resized of if a new disk was placed '''
        self._canvas.delete(tkinter.ALL)
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        deltax = canvas_width / othello_logic_gui.game.get_column(self._game)
        deltay = canvas_height / othello_logic_gui.game.get_row(self._game)
        for x in range(othello_logic_gui.game.get_column(self._game)):
            self._canvas.create_line(x*deltax, 0, x*deltax, canvas_height,fill = 'black')
        for y in range(othello_logic_gui.game.get_row(self._game)):
            self._canvas.create_line(0, y*deltay, canvas_width, y*deltay,fill = 'black')
        for row in range(len(othello_logic_gui.game.get_board(self._game))):
            for col in range(len(othello_logic_gui.game.get_board(self._game)[row])):
                if othello_logic_gui.game.get_board(self._game)[row][col] == 1:
                    x1 = col * deltax
                    x2 = (col + 1) * deltax
                    y1 = row * deltay
                    y2 = (row + 1) * deltay
                    self._canvas.create_oval(x1, y1, x2, y2, fill = 'black')
                elif othello_logic_gui.game.get_board(self._game)[row][col] == 2:
                    x1 = col * deltax
                    x2 = (col + 1) * deltax
                    y1 = row * deltay
                    y2 = (row + 1) * deltay
                    self._canvas.create_oval(x1, y1, x2, y2, fill = 'white')
        
    def _mouse_clicked(self, event:tkinter.Event):
        ''' Handles any mouse click. Such as if the user wants to put down a disc. '''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        click_point = point.Point(event.x, event.y, width, height,othello_logic_gui.game.get_row(self._game),othello_logic_gui.game.get_column(self._game))
        see_row = click_point.check_row()
        see_column = click_point.check_column()
        ccc = othello_logic_gui.game.go(self._game, see_row, see_column,False)
        if True in ccc and othello_logic_gui.game.check_if_empty(self._game, see_row, see_column) == True:
            othello_logic_gui.game.go(self._game, see_row, see_column,True)
            self._update_scoreboard()        
            self._redraw_board()
            if self._mode == "CPU":
                print(self.num)
                self.num += 1
                ai = othello_logic_gui.AI(self._game)
                row, col = ai.chooseMove()
                othello_logic_gui.game.go(self._game, row, col,True)
                self._update_scoreboard()        
                self._redraw_board()
                
        if othello_logic_gui.game.see_winner(self._game) != None:
                self._winner_scoreboard()        
                self._redraw_board()
                self._winner()
        else: 
            if othello_logic_gui.game.lets_see(self._game) == False:
                self._update_scoreboard()        
                self._redraw_board()
                self._skipped_turn()
            
                
    def _winner(self):
        ''' Opens a new toplevel window once the game is over and asks the user if they want to play a new game'''
        self._dialog_window = tkinter.Toplevel()
        self._dialog_window.title('WINNER')
        win_message = tkinter.Label(master = self._dialog_window, text = othello_logic_gui.game.see_winner(self._game), font = DEFAULT_FONT)
        win_message.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        ok_button = tkinter.Button(master =  self._dialog_window, text = 'New Game', font = DEFAULT_FONT, command = self._on_newgame_button)
        ok_button.grid(row = 1, column = 0)
        cancel_button = tkinter.Button(master =  self._dialog_window, text = 'Cancel', font = DEFAULT_FONT, command = self._on_cancel_button)
        cancel_button.grid(row = 1, column = 1)
        self._dialog_window.rowconfigure(0, weight = 1)
        self._dialog_window.rowconfigure(1, weight = 1)
        self._dialog_window.columnconfigure(0, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()
         
    def _on_newgame_button(self):
        ''' Destroys the current rootwindow and runs a new game options window '''
        self._root_window.destroy()
        start().run()
              
    def _on_cancel_button(self):
        ''' Destroys the root window '''
        self._root_window.destroy()
        
    def _skipped_turn(self):
        ''' Opens a new toplevel window saying that the player is skipped'''
        self._skip_window = tkinter.Toplevel()
        self._skip_window.title('Skipped')
        skip_message = tkinter.Message(master = self._skip_window, text = othello_logic_gui.game.skip_turn(self._game) + ' is skipped', font = DEFAULT_FONT, width = 300)
        skip_message.grid(row = 0, column = 0, sticky = tkinter.S + tkinter.N + tkinter.E + tkinter.W)
        ok_button = tkinter.Button(master =  self._skip_window, text = 'OK', font = DEFAULT_FONT, command = self._on_skip_ok)
        ok_button.grid(row = 1, column = 0, sticky = tkinter.N + tkinter.S)
        self._skip_window.rowconfigure(0, weight = 1)
        self._skip_window.rowconfigure(1, weight = 1)
        self._skip_window.columnconfigure(0, weight = 1)
        self._skip_window.grab_set()
        self._skip_window.wait_window()
        
    def _on_skip_ok(self):
        ''' Destroys the skip window '''
        self._skip_window.destroy()

    def run(self) -> None:
        ''' Runs the main game '''
        self._root_window.mainloop() 
    
    def _update_scoreboard(self):
        ''' Updates the scoreboard '''
        self._label_black['text'] = 'Black: ' + str(othello_logic_gui.game.get_black(self._game))
        self._label_white['text'] = 'White: ' + str(othello_logic_gui.game.get_white(self._game))
        if othello_logic_gui.game.get_turn(self._game) == 1:
            self._label_turn['text'] = "Black's Turn"
        elif othello_logic_gui.game.get_turn(self._game) == 2:
            self._label_turn['text'] = "White's Turn"
            
    def _winner_scoreboard(self):
        ''' Changes the scoreboard to the winner '''
        self._label_turn['text'] = othello_logic_gui.game.see_winner(self._game)
        
if __name__ == '__main__':
    #game_options().run()
    start().run()
    
