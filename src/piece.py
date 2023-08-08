import pygame
import os


class Piece():

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.value = value
        self.moved_from_start = False
        self.moves = []
        self.texture = texture
        self.texture_rect = texture_rect
        self.pinned = False

    def attach_texture_to_piece(self):
        self.texture = os.path.join(
            f'./assets/imgs/{self.color}-{self.name}.png')

    def clear_moves_list(self):
        self.moves = []

    def add_move(self, move):
        self.moves.append(move)


class Pawn(Piece):
    def __init__(self, color):
        self.direction = -8 if color == 'white' else 8
        self.en_passant = False
        super().__init__('pawn', color, 100.0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 320.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 330.0)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 500.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 900.0)


class King(Piece):
    def __init__(self, color):
        self.cant_castle_kingside = False
        self.cant_castle_queenside = False
        super().__init__('king', color, 20000.0)
