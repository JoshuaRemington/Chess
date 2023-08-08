from piece import Piece
from constants import *
import pygame


class Mouse():

    def __init__(self):
        self.grab_piece = False
        self.piece = None
        self.mouseX = None
        self.mouseY = None
        self.initial_row = None
        self.initial_col = None
        self.location = None
        self.initial_location = None

    def pickup_piece(self, piece, pos):
        self.grab_piece = True
        self.piece = piece
        self.initial_col = pos[0] // SQSIZE
        self.initial_row = pos[1] // SQSIZE
        self.initial_location = self.initial_col + (self.initial_row * 8)

    def update_mouse_location(self, mouse_pos, screen):
        if mouse_pos is not None:
            self.mouseX, self.mouseY = mouse_pos
            self.initial_col = mouse_pos[0] // SQSIZE
            self.initial_row = mouse_pos[1] // SQSIZE
            self.location = self.initial_col + (self.initial_row * 8)
        if self.piece is not None:
            self.piece.attach_texture_to_piece()
            img = pygame.image.load(self.piece.texture)
            img_cent = (self.mouseX, self.mouseY)
            self.piece.texture_rect = img.get_rect(center=img_cent)
            screen.blit(img, self.piece.texture_rect)

    def release_mouse(self):
        self.grab_piece = False
        self.piece = None
