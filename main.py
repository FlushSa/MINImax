import sys
import copy
import pygame
import numpy as np
import random
from data import *



pygame.init()
obraz = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption('Piškvorky')
obraz.fill(POZADI)

class Board:

    def __init__(self):
        self.square = np.zeros((ROW, COLUMN))
        self.marked_sqr = 0

    def mark_sqr(self, row, column, player):
        self.square[row][column] = player
        self.marked_sqr += 1

    def empty_sqr(self, row, column):
        return self.square[row][column] == 0

    def get_empty_sqr(self):
        empty_sqr = []
        for row in range(ROW):
            for column in range(COLUMN):
                if self.empty_sqr(row, column):
                    empty_sqr.append ((row, column))
        return empty_sqr

    

    def winner(self, show=False):
    # svislé
        for column in range(COLUMN):
            for row in range(ROW - 3):
                if self.square[row][column] == self.square[row + 1][column] == self.square[row + 2][column] == self.square[row + 3][column] != 0:
                    if show:
                        start = (column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        end = (column * SQSIZE + SQSIZE // 2, (row + 4) * SQSIZE - SQSIZE // 2)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.square[row][column]

        # vodorovné
        for row in range(ROW):
            for column in range(COLUMN - 3):
                if self.square[row][column] == self.square[row][column + 1] == self.square[row][column + 2] == self.square[row][column + 3] != 0:
                    if show:
                        start = (column * SQSIZE + SQSIZE // 4, row * SQSIZE + SQSIZE // 2)
                        end = ((column + 4) * SQSIZE - SQSIZE // 4, row * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.square[row][column]

        # diagonály
        for row in range(ROW - 3):
            for column in range(COLUMN - 3):
                if self.square[row][column] == self.square[row + 1][column + 1] == self.square[row + 2][column + 2] == self.square[row + 3][column + 3] != 0:
                    if show:
                        start = (column * SQSIZE + SQSIZE // 4, row * SQSIZE + SQSIZE // 4)
                        end = ((column + 4) * SQSIZE - SQSIZE // 4, (row + 4) * SQSIZE - SQSIZE // 4)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.square[row][column]

        for row in range(ROW - 3):
            for column in range(3, COLUMN):
                if self.square[row][column] == self.square[row + 1][column - 1] == self.square[row + 2][column - 2] == self.square[row + 3][column - 3] != 0:
                    if show:
                        start = ((column + 1/ 2) * SQSIZE + SQSIZE // 4, row * SQSIZE + SQSIZE // 4)
                        end = ((column - 3) * SQSIZE + SQSIZE // 4, (row + 4) * SQSIZE - SQSIZE // 4)
                        pygame.draw.line(obraz, LINE_COLOR, start, end, LINE_WIDTH)
                    return self.square[row][column]

        return 0



    def full(self):
        return self.marked_sqr == 36

    def empty(self):
        return self.marked_sqr == 0

class Minimax:
    def __init__(self, depth):
        self.depth = depth
        print("Minimax initialized with depth:", depth)

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        print("Minimax minimax called with depth:", depth)
        if depth == 0 or board.full() or board.winner():
            return None, self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in board.get_empty_sqr():
                board.mark_sqr(move[0], move[1], 2)
                _, eval = self.minimax(board, depth - 1, False, alpha, beta)
                board.mark_sqr(move[0], move[1], 0)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                print("Alpha:", alpha)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in board.get_empty_sqr():
                board.mark_sqr(move[0], move[1], 1)
                _, eval = self.minimax(board, depth - 1, True, alpha, beta)
                board.mark_sqr(move[0], move[1], 0)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                print("Beta:", beta)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def evaluate(self, board):
        print("Minimax evaluate called")
        winner = board.winner()
        if winner == 2:
            return 100
        elif winner == 1:
            return -100
        else:
            return 0
   


class Game:

    def __init__(self):
        self.board = Board()
        self.player = random.choice ([1,2])
        self.running = True
        self.show_lines()
        self.minimax = Minimax(depth=10)


       
        #Čáry na rozdělení desky
    def show_lines(self):

        obraz.fill(POZADI)
        
        #Diagonální 
        for i in range(1, 6):
            x = i * SQSIZE
            pygame.draw.line(obraz, LINE_COLOR, (x, 0), (x, VYSKA), LINE_WIDTH)

            #Vodorovné
        for i in range(1, 6):
            y = i * SQSIZE
            pygame.draw.line(obraz, LINE_COLOR, (0, y), (SIRKA, y), LINE_WIDTH)


        #Přehazování hráčů (křížek a kolečko)
   
    def next_turn(self):
        self.player = self.player % 2 + 1

        
        # Hráč 1 - kříž
   
    def figures(self, row, column):
        if self.player == 1:
            start = (column * SQSIZE + ODSAZENI, row * SQSIZE + ODSAZENI)
            end = (column * SQSIZE + SQSIZE - ODSAZENI, row * SQSIZE + SQSIZE - ODSAZENI)

            pygame.draw.line(obraz, CROSS_COLOR, start, end, CROSS_WIDTH)
            pygame.draw.line(obraz, CROSS_COLOR, (start[0], end[1]), (end[0], start[1]), CROSS_WIDTH)

        # Hráč 2 - kolečko
        elif self.player == 2:
            center = (column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(obraz, CIRC_COLOR, center, PRUMER, CIRC_WIDTH)

        # definování funkce, kdy končí
   
    def ending(self):
        return self.board.winner(show=True) != 0 or self.board.full()
    
    def reset(self):
        self.__init__()
    
    def make_move(self, row, column):
        if self.player == 1 and self.board.empty_sqr(row, column):
            self.board.mark_sqr(row, column, self.player)
            self.figures(row, column)
            self.next_turn()
            if self.ending():
                self.running = False
            else:
                self.ai_move()

    def ai_move(self):
        if self.running:
            print("AI player's move - Before minimax")  # Add this line for debugging
            move, _ = self.minimax.minimax(self.board, self.minimax.depth, True, float('-inf'), float('inf'))
            print("AI player's move - After minimax")  # Add this line for debugging
            print("Selected move:", move)  # Add this line for debugging
            if move:
                self.board.mark_sqr(move[0], move[1], 2)
                self.figures(move[0], move[1])
                self.next_turn()
                if self.ending():
                    self.running = False

def main():
    try:
        game = Game()
        board = game.board

        while True:
            print("Inside game loop")  # Add this line for debugging
            # pygame events
            for event in pygame.event.get():
                print("Handling pygame event")  # Add this line for debugging

                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # keydown event
                if event.type == pygame.KEYDOWN:

                    # r-restart
                    if event.key == pygame.K_r:
                        game.reset()
                        board = game.board

                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    column = pos[0] // SQSIZE
                    
                    # human mark sqr
                    if board.empty_sqr(row, column) and game.running:
                        print("Human player's move")
                        game.make_move(row, column)
                        if game.ending():
                            game.running = False
                            print("Game ended")

                        pygame.display.flip()  # Update display after human move

                        print("AI player's move")
                        game.ai_move()
                        if game.ending():
                            game.running = False
                            print("Game ended")

                        pygame.display.flip()  # Update display after AI move

            pygame.display.update()

    except Exception as e:
        print("An error occurred:", e)
        pygame.quit()
        sys.exit(1)

main()