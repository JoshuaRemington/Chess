from constants import *
import pygame
from board import Board
from mouse import Mouse
from menu import Menu
from piece import *
from square import Square
from move import Move


class Game_Setup():

    def __init__(self):
        self.board = Board()
        self.squares = self.board.squares
        self.current_turn = 'None'
        self.mouse = Mouse()
        self.menu = Menu()
        self.hovering = None
        self.__put_start_pieces_in_location()
        self.board.get_all_moves(None)

    def render_side(self, screen):
        color = SIDE_COLOR
        rect = (800, 0, 400, 800)
        pygame.draw.rect(screen, color, rect)

    def render_squares_on_board(self, screen):
        for col in range(COLS):
            for row in range(ROWS):
                color = SQUARE_ONE_COLOR if (
                    col+row) % 2 == 0 else SQUARE_TWO_COLOR
                rect = (row*SQSIZE, col*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(screen, color, rect)

    def render_pieces_on_board(self, screen):
        for i in self.board.squares:
            if i.has_piece():
                if i.piece != self.mouse.piece:
                    piece = i.piece
                    piece.attach_texture_to_piece()
                    img = pygame.image.load(piece.texture)
                    img = pygame.transform.scale(img, (SQSIZE, SQSIZE))
                    img_cent = (i.location % 8) * \
                        SQSIZE + SQSIZE // 2, (i.location // 8) * \
                        SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_cent)
                    screen.blit(img, piece.texture_rect)

    def render_available_moves_for_piece(self, screen):
        if self.mouse.grab_piece:
            piece = self.mouse.piece
            if piece == None:
                return
            for move in piece.moves:
                color = POTENTIAL_MOVE_COLOR if (
                    move.final_loc.location) % 2 == 0 else POTENTIAL_MOVE_COLOR_TWO
                move_rect = (move.final_loc.location % 8) * \
                    SQSIZE, (move.final_loc.location // 8) * \
                    SQSIZE, SQSIZE, SQSIZE
                pygame.draw.rect(screen, color, move_rect)

    def render_last_move(self, screen):
        if self.board.last_move:
            initial = (self.board.last_move.initial_loc.location)
            final = (self.board.last_move.final_loc.location)
            for pos in [initial, final]:
                color = LAST_MOVE_COLOR
                rect = ((pos % 8) * SQSIZE, (pos // 8)
                        * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(screen, color, rect, 5)

    def change_turn(self):
        if self.current_turn == 'white':
            self.current_turn = 'black'
        else:
            self.current_turn = 'white'
        self.board.get_all_moves(None)

    def __put_start_pieces_in_location(self):
        self.fen_to_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq')

    def fen_to_board(self, fen):
        current_loc = -1
        side_to_move = None
        black_king_castling = False
        black_queen_castling = False
        white_king_castling = False
        white_queen_castling = False
        for i in fen:
            current_loc += 1
            if current_loc < 64:
                match i:
                    case 'p':
                        self.squares[current_loc] = Square(
                            current_loc, Pawn('black'))
                    case 'b':
                        self.squares[current_loc] = Square(
                            current_loc, Bishop('black'))
                    case 'n':
                        self.squares[current_loc] = Square(
                            current_loc, Knight('black'))
                    case 'k':
                        self.squares[current_loc] = Square(
                            current_loc, King('black'))
                    case 'q':
                        self.squares[current_loc] = Square(
                            current_loc, Queen('black'))
                    case 'r':
                        self.squares[current_loc] = Square(
                            current_loc, Rook('black'))
                    case 'P':
                        self.squares[current_loc] = Square(
                            current_loc, Pawn('white'))
                    case 'B':
                        self.squares[current_loc] = Square(
                            current_loc, Bishop('white'))
                    case 'N':
                        self.squares[current_loc] = Square(
                            current_loc, Knight('white'))
                    case 'K':
                        self.squares[current_loc] = Square(
                            current_loc, King('white'))
                    case 'Q':
                        self.squares[current_loc] = Square(
                            current_loc, Queen('white'))
                    case 'R':
                        self.squares[current_loc] = Square(
                            current_loc, Rook('white'))
                    case '/':
                        current_loc -= 1
                    case _:
                        current_loc += int(i) - 1

            else:
                if i == ' ' or i == '-' or i == '0' or i == '1':
                    pass
                elif not side_to_move:
                    if i == 'w':
                        side_to_move = True
                        self.current_turn = 'white'
                    elif i == 'b':
                        side_to_move = True
                        self.current_turn = 'black'
                elif i == 'K':
                    white_king_castling = True
                elif i == 'Q':
                    white_queen_castling = True
                elif i == 'k':
                    black_king_castling = True
                elif i == 'q':
                    black_queen_castling = True
                else:
                    if i == 'a':
                        column = 1
                    elif i == 'b':
                        column = 2
                    elif i == 'c':
                        column = 3
                    elif i == 'd':
                        column = 4
                    elif i == 'e':
                        column = 5
                    elif i == 'f':
                        column = 6
                    elif i == 'g':
                        column = 7
                    elif i == 'h':
                        column = 8
                    elif i == '6':
                        if self.squares[23+column].piece and self.squares[23+column].piece.name == 'pawn':
                            self.squares[23+column].piece.en_passant = True
                            self.board.last_move = Move(
                                Square(7+column), Square(23+column))
                    elif i == '3':
                        if self.squares[31+column].piece and self.squares[31+column].piece.name == 'pawn':
                            self.squares[31+column].piece.en_passant = True
                            self.board.last_move = Move(
                                Square(47+column), Square(31+column))

        if not white_king_castling and self.squares[63].piece:
            self.squares[63].piece.moved_from_start = True
        if not white_queen_castling and self.squares[56].piece:
            self.squares[56].piece.moved_from_start = True
        if not black_king_castling and self.squares[7].piece:
            self.squares[7].piece.moved_from_start = True
        if not black_queen_castling and self.squares[1].piece:
            self.squares[1].piece.moved_from_start = True
