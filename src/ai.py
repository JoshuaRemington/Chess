from typing import Any
from gameSetup import Game_Setup
from constants import *
import random
import pygame
import copy
from piece import *


class AI():

    def __init__(self):
        self.game = Game_Setup()
        self.color = 'none'
        self.ai_mode = 'Random Moves'
        self.testing_moves_checked = 0

    def cycle_ai_type(self):
        if self.ai_mode == 'Simple AI':
            self.ai_mode = 'Random Moves'
            self.ai_mode = 'Beginner Bot'
        elif self.ai_mode == 'Random Moves':
            self.ai_mode = 'Simple AI'
        else:
            self.ai_mode = 'Random Moves'

    def play_random_move(self):
        if self.color == 'white':
            moves = self.game.board.white_moves
        else:
            moves = self.game.board.black_moves

        if not moves:
            return

        max = len(moves) - 1

        while True:
            random_move = moves[random.randint(0, max)]
            piece = self.game.board.squares[random_move.initial_loc.location].piece
            if piece.color == self.color:
                break
        self.game.board.make_move(random_move, piece)
        piece.moved_from_start = True
        self.game.board.last_move = random_move

    def beginner_ai(self):
        self.testing_moves_checked = 0
        best_move = None
        best_score = float('inf')
        self.game.board.get_all_moves(None)

        if self.color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -100000
            return 0

        for mov in moves:
            ai = copy.deepcopy(self)
            game = ai.game
            piece = game.board.squares[mov.initial_loc.location].piece
            ai.game.board.make_move(mov, piece, True)
            score = self.alpha_beta(
                ai, 2, -float('inf'), float('inf'), True, opp_color)
            if score < best_score:
                best_score = score
                best_move = mov
            self.testing_moves_checked += 1

        piece = self.game.board.squares[best_move.initial_loc.location].piece

        self.game.board.make_move(best_move, piece)
        piece.moved_from_start = True
        self.game.board.last_move = best_move

        if self.game.board.promoting_pawn:
            self.game.board.promotion_square.piece = Queen(piece.color)
            self.game.board.promoting_pawn = False

        return 1

    def alpha_beta(self, copy_ai, depth, alpha, beta, maximizing, color):
        if depth == 0:
            return copy_ai.game.board.evaluate_board(color)

        copy_ai.game.board.get_all_moves(None)

        if color == 'white':
            moves = copy_ai.game.board.white_moves
            opp_color = 'black'
        else:
            moves = copy_ai.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -100000
            return 0

        if maximizing:
            best_score = -float('inf')
            for move in moves:
                copy_of_copy = copy.deepcopy(copy_ai)
                game = copy_of_copy.game
                piece = game.board.squares[move.initial_loc.location].piece
                copy_of_copy.game.board.make_move(move, piece, True)

                best_score = max(best_score, self.alpha_beta(
                    copy_of_copy, depth-1, beta, alpha, False, opp_color))
                alpha = max(alpha, best_score)
                self.testing_moves_checked += 1
                if beta <= alpha:
                    return best_score
            return best_score
        else:
            best_score = float('inf')
            for move in moves:
                copy_of_copy = copy.deepcopy(copy_ai)
                game = copy_of_copy.game
                piece = game.board.squares[move.initial_loc.location].piece
                copy_of_copy.game.board.make_move(move, piece, True)

                best_score = min(best_score, self.alpha_beta(
                    copy_of_copy, depth-1, alpha, beta, True, opp_color))
                beta = min(beta, best_score)
                self.testing_moves_checked += 1
                if beta <= alpha:
                    return best_score
            return best_score

    def simple_ai(self):
        self.game.board.get_all_moves(None)
        current_move = None
        if self.color == 'white':
            moves = self.game.board.white_moves
        else:
            moves = self.game.board.black_moves

        if not moves:
            return

        current_max = -10000

        for mov in moves:
            piece = self.game.board.squares[mov.initial_loc.location].piece
            moved_before = piece.moved_from_start
            self.game.board.make_move(mov, piece)
            if self.color == 'white':
                white_advantage = self.game.board.evaluate_board('white')
                if white_advantage > current_max:
                    current_max = white_advantage
                    current_move = mov
            else:
                black_advantage = self.game.board.evaluate_board('black')
                if black_advantage > current_max:
                    current_max = black_advantage
                    current_move = mov
            self.game.board.unmake_move(mov, piece, True)
            piece.moved_from_start = moved_before

        piece = self.game.board.squares[current_move.initial_loc.location].piece

        self.game.board.make_move(current_move, piece)
        piece.moved_from_start = True
        self.game.board.last_move = current_move

        if self.game.board.promoting_pawn:
            self.game.board.promotion_square.piece = Queen(piece.color)
            self.game.board.promoting_pawn = False

    def dislpay_ai_type(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Current AI:", True, TEXT_COLOR)
        screen.blit(text, (815, 650))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.ai_mode, True, TEXT_COLOR)
        screen.blit(text, (815, 700))

    def reset(self):
        self.__init__()


'''
    def beginner_ai(self):
        self.testing_moves_checked = 0
        best_move = None
        best_score = float('inf')
        self.game.board.get_all_moves(None)

        if self.color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -100000
            return 0

        for mov in moves:
            ai = copy.deepcopy(self)
            game = ai.game
            piece = game.board.squares[mov.initial_loc.location].piece
            ai.game.board.make_move(mov, piece)
            score = self.alpha_beta(
                ai, 1, -float('inf'), float('inf'), True, opp_color)
            if score < best_score:
                best_score = score
                best_move = mov
            self.testing_moves_checked += 1

        piece = self.game.board.squares[best_move.initial_loc.location].piece

        self.game.board.make_move(best_move, piece)
        piece.moved_from_start = True
        self.game.board.last_move = best_move

        if self.game.board.promoting_pawn:
            self.game.board.promotion_square.piece = Queen(piece.color)
            self.game.board.promoting_pawn = False

        return 1

    def alpha_beta(self, copy_ai, depth, alpha, beta, maximizing, color):
        if depth == 0 and color == 'black':
            return copy_ai.game.board.evaluate_board('white')
        elif depth == 0:
            return copy_ai.game.board.evaluate_board('black')

        copy_ai.game.board.get_all_moves(None)

        if color == 'white':
            moves = copy_ai.game.board.white_moves
            opp_color = 'black'
        else:
            moves = copy_ai.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -100000
            return 0

        if maximizing:
            best_score = -float('inf')
            for move in moves:
                copy_of_copy = copy.deepcopy(copy_ai)
                game = copy_of_copy.game
                piece = game.board.squares[move.initial_loc.location].piece
                copy_of_copy.game.board.make_move(move, piece)

                best_score = max(best_score, self.alpha_beta(
                    copy_of_copy, depth-1, alpha, beta, False, opp_color))
                alpha = max(alpha, best_score)
                self.testing_moves_checked += 1
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in moves:
                copy_of_copy = copy.deepcopy(copy_ai)
                game = copy_of_copy.game
                piece = game.board.squares[move.initial_loc.location].piece
                copy_of_copy.game.board.make_move(move, piece)

                best_score = min(best_score, self.alpha_beta(
                    copy_of_copy, depth-1, alpha, beta, True, opp_color))
                beta = min(beta, best_score)
                self.testing_moves_checked += 1
                if beta <= alpha:
                    break
            return best_score
'''

'''
def beginner_ai(self):
        if self.color == 'black':
            color = 'black'
        else:
            color = 'white'

        self.testing_moves_checked = 0

        self.game.board.get_all_moves(None)

        if color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        max = -float('inf')
        test = 0

        for move in moves:
            self.testing_moves_checked += 1
            piece = self.game.board.squares[move.initial_loc.location].piece
            moved_before = piece.moved_from_start
            self.game.board.make_move(move, piece)
            score = self.nega_max(1, opp_color)
            self.game.board.unmake_move(move, piece)
            piece.moved_from_start = moved_before
            if score > max:
                max = score
                best_move = move
            if self.game.board.squares[55].piece and self.game.board.squares[55].piece.name == 'knight':
                test += 1
                print(test)

        piece = self.game.board.squares[best_move.initial_loc.location].piece

        self.game.board.make_move(best_move, piece)
        print(piece, best_move.initial_loc.location, max)
        piece.moved_from_start = True
        self.game.board.last_move = best_move

        if self.game.board.promoting_pawn:
            self.game.board.promotion_square.piece = Queen(piece.color)
            self.game.board.promoting_pawn = False

        return 1

    def nega_max(self, depth, color):
        if depth == 0 and color == 'black':
            return self.game.board.evaluate_board('white')
        elif depth == 0:
            return self.game.board.evaluate_board('black')

        self.game.board.get_all_moves(None)

        if color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -10000
            return 10000

        max = -float('inf')

        for move in moves:
            self.testing_moves_checked += 1
            piece = self.game.board.squares[move.initial_loc.location].piece
            moved_before = piece.moved_from_start
            self.game.board.make_move(move, piece)
            score = -self.nega_max(depth-1, opp_color)
            self.game.board.unmake_move(move, piece)
            piece.moved_from_start = moved_before
            if score > max:
                max = score

        return max
        '''


'''
    def beginner_ai(self):
        self.game.board.get_all_moves(None)
        king_position = self.get_king_position()
        self.testing_moves_checked = 0
        best_move = None
        best_score = float('inf')

        if self.color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -100000
            return 0

        for mov in moves:
            piece = self.game.board.squares[mov.initial_loc.location].piece
            if not piece:
                print('why isnt this working')
            if False:
                pass
            else:
                moved_before = piece.moved_from_start
                self.game.board.make_move(mov, piece)
                score = self.alpha_beta(
                    1, -float('inf'), float('inf'), True, opp_color)
                self.game.board.unmake_move(mov, piece, True)
                piece.moved_from_start = moved_before
                if score < best_score:
                    best_score = score
                    best_move = mov
                self.testing_moves_checked += 1

        self.fix_king_error(king_position)

        piece = self.game.board.squares[best_move.initial_loc.location].piece

        self.game.board.make_move(best_move, piece)
        piece.moved_from_start = True
        self.game.board.last_move = best_move

        if self.game.board.promoting_pawn and self.game.board.promoting_pawn_color == self.color:
            self.game.board.promotion_square.piece = Queen(piece.color)
            self.game.board.promoting_pawn = False

        return 1

    def alpha_beta(self, depth, alpha, beta, maximizing, color):
        if depth == 0 and color == 'black':
            return self.game.board.evaluate_board('white')
        elif depth == 0:
            return self.game.board.evaluate_board('black')

        if color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        if not moves:
            if self.game.board.in_check != 'None':
                return -100000
            return 0

        if maximizing:
            best_score = -float('inf')
            for move in moves:
                piece = self.game.board.squares[move.initial_loc.location].piece
                if piece:
                    print(move.initial_loc.location)
                moved_before = piece.moved_from_start
                self.game.board.make_move(move, piece)
                if self.game.board.promoting_pawn and self.game.board.promoting_pawn_color == color:
                    self.game.board.promotion_square.piece = Queen(piece.color)
                    self.game.board.promoting_pawn = False

                best_score = max(best_score, self.alpha_beta(
                    depth-1, alpha, beta, False, opp_color))
                self.game.board.unmake_move(move, piece, True)
                piece.moved_from_start = moved_before
                alpha = max(alpha, best_score)
                self.testing_moves_checked += 1
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in moves:
                piece = self.game.board.squares[move.initial_loc.location].piece
                if not piece:
                    print(move.initial_loc.location)
                else:
                    print(move.initial_loc.location)
                moved_before = piece.moved_from_start
                self.game.board.make_move(move, piece)
                if self.game.board.promoting_pawn and self.game.board.promoting_pawn_color == color:
                    self.game.board.promotion_square.piece = Queen(piece.color)
                    self.game.board.promoting_pawn = False

                best_score = min(best_score, self.alpha_beta(
                    depth-1, alpha, beta, True, opp_color))
                self.game.board.unmake_move(move, piece, True)
                piece.moved_from_start = moved_before
                beta = min(beta, best_score)
                self.testing_moves_checked += 1
                if beta <= alpha:
                    break
            return best_score 
            '''

'''def fix_king_error(self, pos):
        for i in self.game.board.squares:
            if i.location != pos:
                if i.piece and isinstance(i.piece, King) and i.piece.color == self.color:
                    i.piece = None
            else:
                i.piece = King(self.color)

    def get_king_position(self):
        for i in self.game.board.squares:
            if i.piece and isinstance(i.piece, King) and i.piece.color == self.color:
                return i.location

    def beginner_ai(self):
        copy_ = copy.deepcopy(self.game.board.squares)
        move = self.minimax_root(2)
        piece = self.game.board.squares[move.initial_loc.location].piece
        self.game.board.squares = copy_
        self.game.board.make_move(move, piece)

    def minimax_root(self, depth):
        self.testing_moves_checked = 0
        best_move_score = -9999
        best_move = None
        if self.color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        for mov in moves:
            self.testing_moves_checked += 1
            piece = self.game.board.squares[mov.initial_loc.location].piece
            piece_has_moved = piece.moved_from_start
            self.game.board.make_move(mov, piece)
            value = max(best_move_score, self.minimax(
                depth-1, opp_color))
            self.game.board.unmake_move(mov, piece, True)
            piece.moved_from_start = piece_has_moved
            if value > best_move_score:
                best_move_score = value
                best_move = mov

        return best_move

    def minimax(self, depth, color):
        if depth == 0 and color == 'black':
            return self.game.board.evaluate_board('white')
        elif depth == 0:
            return self.game.board.evaluate_board('black')

        self.game.board.get_all_moves(None)

        if color == 'white':
            moves = self.game.board.white_moves
            opp_color = 'black'
        else:
            moves = self.game.board.black_moves
            opp_color = 'white'

        best_move_score = -9999
        for mov in moves:
            self.testing_moves_checked += 1
            piece = self.game.board.squares[mov.initial_loc.location].piece
            piece_has_moved = piece.moved_from_start
            self.game.board.make_move(mov, piece)
            value = -max(best_move_score, self.minimax(
                depth-1, opp_color))
            self.game.board.unmake_move(mov, piece)
            piece.moved_from_start = piece_has_moved
            if value > best_move_score:
                best_move_score = value

        return best_move_score'''
