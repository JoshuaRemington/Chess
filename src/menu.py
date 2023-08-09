import pygame
from constants import *


class Menu():

    def __init__(self):
        pass

    def keyboard_shortcuts(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Keyboard Shortuts:', True, TEXT_COLOR)
        screen.blit(text, (815, 50))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('r - Restart Game', True, TEXT_COLOR)
        screen.blit(text, (815, 100))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('p - Player VS. Player', True, TEXT_COLOR)
        screen.blit(text, (815, 150))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('c - Change Bot Type', True, TEXT_COLOR)
        screen.blit(text, (815, 200))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('w - Play Bot as white', True, TEXT_COLOR)
        screen.blit(text, (815, 250))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('b - Play Bot as black', True, TEXT_COLOR)
        screen.blit(text, (815, 300))
