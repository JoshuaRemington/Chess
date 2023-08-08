import pygame
import sys
from constants import *
from ai import AI
from gameSetup import Game_Setup
from mouse import Mouse
from square import Square
from move import Move
import time


class test():
    def __init__(self, val):
        self.val = val


class Main():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ai = AI()
        self.game = self.ai.game
        self.board = self.ai.game.board
        self.mouse = self.ai.game.mouse
        self.menu = self.ai.game.menu

    def run_Main(self):
        ai = self.ai
        screen = self.screen
        game = self.game
        mouse = self.mouse
        board = self.board
        menu = self.menu
        while True:
            game.render_squares_on_board(screen)
            game.render_last_move(screen)
            game.render_available_moves_for_piece(screen)
            game.render_pieces_on_board(screen)
            mouse.update_mouse_location(None, screen)
            game.render_side(screen)
            menu.keyboard_shortcuts(screen)
            ai.dislpay_ai_type(screen)
            if board.promoting_pawn:
                game.render_side(screen)
                board.render_pawn_promote(screen)
            if board.generate_new_moves and not board.promoting_pawn:
                board.get_all_moves(None)

            if game.current_turn == ai.color and not board.promoting_pawn:
                if ai.ai_mode == 'Random Moves':
                    time.sleep(1)
                    ai.play_random_move()
                elif ai.ai_mode == 'Simple AI':
                    time.sleep(1)
                    ai.simple_ai()
                elif ai.ai_mode == 'Beginner Bot':
                    val = ai.beginner_ai()
                    if val == 10000 or val == -10000:
                        game.current_turn = 'None'
                    print(ai.testing_moves_checked)
                    if self.ai.color == 'white':
                        self.ai.color = 'black'
                    else:
                        self.ai.color = 'white'
                game.change_turn()

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse.update_mouse_location(event.pos, screen)
                    if (board.promoting_pawn):
                        board.pawn_promote(event.pos)
                    clicked_location = mouse.location
                    if not Square.out_of_range(event.pos[1] // SQSIZE, event.pos[0] // SQSIZE) and not board.promoting_pawn:
                        if board.squares[clicked_location].has_piece() and board.squares[clicked_location].piece.color == game.current_turn != 'None':
                            piece = board.squares[clicked_location].piece
                            mouse.pickup_piece(piece, event.pos)
                            game.render_available_moves_for_piece(screen)
                elif event.type == pygame.MOUSEMOTION:
                    mouse.update_mouse_location(event.pos, screen)
                    if not Square.out_of_range(mouse.location):
                        if mouse.grab_piece:
                            game.render_squares_on_board(screen)
                            game.render_last_move(screen)
                            game.render_available_moves_for_piece(screen)
                            game.render_pieces_on_board(screen)
                            mouse.update_mouse_location(event.pos, screen)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if mouse.grab_piece:
                        mouse.update_mouse_location(None, screen)
                        initial = Square(mouse.initial_location)
                        final = Square(mouse.location)
                        move = Move(initial, final)
                        if board.move_is_valid(mouse.piece, move):
                            mouse.release_mouse()
                            board.make_move(move, piece)
                            piece.moved_from_start = True
                            board.last_move = move
                            game.render_squares_on_board(screen)
                            game.render_pieces_on_board(screen)
                            game.change_turn()
                    mouse.release_mouse()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        ai_color = ai.color
                        ai.reset()
                        ai = self.ai
                        game = self.ai.game
                        board = self.ai.game.board
                        mouse = self.ai.game.mouse
                        ai.color = ai_color
                        game.current_turn = "white"
                        board.get_all_moves(None)

                    elif event.key == pygame.K_p:
                        ai.reset()
                        ai = self.ai
                        game = self.ai.game
                        board = self.ai.game.board
                        mouse = self.ai.game.mouse
                        ai.color = 'none'
                        game.current_turn = "white"
                        board.get_all_moves(None)

                    elif event.key == pygame.K_c:
                        ai.cycle_ai_type()

                    elif event.key == pygame.K_w:
                        cur_ai = ai.ai_mode
                        ai.reset()
                        ai = self.ai
                        game = self.ai.game
                        board = self.ai.game.board
                        mouse = self.ai.game.mouse
                        ai.ai_mode = cur_ai
                        ai.color = 'black'
                        game.current_turn = 'white'
                        board.get_all_moves(None)

                    elif event.key == pygame.K_b:
                        cur_ai = ai.ai_mode
                        ai.reset()
                        ai = self.ai
                        game = self.ai.game
                        board = self.ai.game.board
                        mouse = self.ai.game.mouse
                        ai.ai_mode = cur_ai
                        ai.color = 'white'
                        game.current_turn = 'white'
                        board.get_all_moves(None)

            pygame.display.update()


main = Main()
main.run_Main()
