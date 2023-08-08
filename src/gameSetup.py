from constants import *
import pygame
from board import Board
from mouse import Mouse
from menu import Menu


class Game_Setup():

    def __init__(self):
        self.board = Board()
        self.current_turn = 'None'
        self.mouse = Mouse()
        self.menu = Menu()
        self.hovering = None

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
