import pygame
import sys
import numpy as np
import random
import copy

WIDTH=500
HEIGHT=500
ROWS=3
COLUMNS=3
SQSIZE=HEIGHT//ROWS
LINE_WIDTH=10
LINE_COLOR=(0,0,0)
BG_COLOR=(0,255,255)
CIRCLE_COLOR=(255,255,255)
CIRCLE_WIDTH=10
RADIUS=SQSIZE//4
CROSS_COLOR=(255,255,255)
CROSS_WIDTH=25
OFFSET=50
pygame.init()  #initialize pygame
screen=pygame.display.set_mode( (WIDTH,HEIGHT) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares=np.zeros((ROWS,COLUMNS))
        self.empty_sqrs=self.squares
        self.marked_sqrs=0
    def final_state(self):

        for col in range(COLUMNS):                                            #vertical winning
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                return self.squares[0][col]
        for row in range(ROWS):                                            #horizontal winning
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                return self.squares[row][0]
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2] !=0:     #desc diagonal winning
            return self.squares[1][1] 
        if self.squares[2][0]==self.squares[1][1]==self.squares[0][2] !=0:     #asc diagonal winning
            return self.squares[1][1] 
          
        return 0                                      
            
    def mark_sqr(self,row,col,player):
        self.squares[row][col]=player
        self.marked_sqrs==1
    def empty_sqr(self,row,col):
        return self.squares[row][col]==0
    def get_emptysqrs(self):
        empty_sqrs=[]
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    def isfull(self):
        return self.marked_sqrs==9
    def isempty(self):
        return self.marked_sqrs==0
    
class AI:
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player

    def rndm(self,board):
        empty_sqrs=board.get_emptysqrs()
        indx=random.randrange(0,len(empty_sqrs))
        return empty_sqrs[indx]
    
    def minimax(self,board,maximizing):
        case=board.final_state()
        if case==1:
            return 1,None
        if case==2:
            return -1,None
        elif board.isfull():
            return 0,None
        
        if maximizing:
            max_val=-100
            best_move=None
            empty_sqrs=board.get_emptysqrs()

            for(row,col) in empty_sqrs:
                new_board=copy.deepcopy(board)
                new_board.mark_sqr(row,col,1)
                val=self.minimax(new_board,False)[0]
                if val>max_val :
                    max_val=val
                    best_move=(row,col)

            return max_val,best_move   

        elif not maximizing:
            min_val=100
            best_move=None
            empty_sqrs=board.get_emptysqrs()

            for(row,col) in empty_sqrs:
                new_board=copy.deepcopy(board)
                new_board.mark_sqr(row,col,self.player)
                val=self.minimax(new_board,True)[0]
                if val<min_val :
                    min_val=val
                    best_move=(row,col)

            return min_val,best_move   
    def val(self,main_board):
        if self.level==0:
            val='random'
            move=self.rndm(main_board)
        else:
            val,move=self.minimax(main_board,False)
        print(f'AI has chosen the Square {move} with an val of {val}')

        return move

class Game:
    def __init__(self):
        self.board=Board()
        self.ai=AI()
        self.player=2
        self.gamemode='ai'
        self.running=True
        self.show_lines()
    def show_lines(self):
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)            #vertical
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),LINE_WIDTH)
        
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH)            #horizontal
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),LINE_WIDTH)
    def next_player(self):                                                              #changing turns
        self.player=self.player %2 + 1
    def draw_fig(self,row,col):
        if self.player==1:
            start_desc=(col * SQSIZE+OFFSET,row * SQSIZE+OFFSET)                #Descendent line of cross
            end_desc=(col * SQSIZE+SQSIZE-OFFSET,row * SQSIZE+SQSIZE-OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)

            start_asc=(col * SQSIZE+OFFSET,row * SQSIZE+SQSIZE-OFFSET)                #Ascendent line of cross
            end_asc=(col * SQSIZE+SQSIZE-OFFSET,row * SQSIZE+OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)
        elif self.player==2:
            center=(col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2)
            pygame.draw.circle(screen,CIRCLE_COLOR,center,RADIUS,CIRCLE_WIDTH)
def main():
    game=Game()
    board=game.board
    ai=game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//SQSIZE                        #1 represents the y axis in rows.
                col=pos[0]//SQSIZE

                if board.empty_sqr(row,col):
                 board.mark_sqr(row,col,game.player)
                 game.draw_fig(row,col)
                 game.next_player()
                  

        if game.gamemode=='ai' and game.player==ai.player:
            pygame.display.update()
            row,col=ai.val(board)
            board.mark_sqr(row,col,ai.player)
            game.draw_fig(row,col)
            game.next_player()
        pygame.display.update()       
main()