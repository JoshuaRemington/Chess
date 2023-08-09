
from constants import *
from square import Square
from piece import *
from move import Move
import copy
import numpy as np


class Board():
    last_move = None

    def __init__(self):
        self.squares = np.array([Square(i) for i in range(64)])
        self.promoting_pawn = False
        self.promoting_pawn_color = 'white'
        self.promotion_square = None
        self.generate_new_moves = None
        self.in_check = "None"
        self.white_moves = []
        self.black_moves = []

    '''def fen_to_board(self, fen):
        current_loc = -1
        for i in fen:
            current_loc += 1
            if current_loc != 64:
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
                        current_loc += int(i) - 1'''

    def check_for_checks(self, move_list):
        good_move_list = []
        king_castling_moves = []
        for move in move_list:
            add = True
            piece = self.squares[move.initial_loc.location].piece
            self.make_move(move, piece, True)
            if piece.name == 'pawn':
                if self.promoting_pawn:
                    self.squares[move.final_loc.location].piece = Pawn(
                        piece.color)
            if piece.name == 'king' and abs(move.final_loc.location - move.initial_loc.location) == 2:
                king_castling_moves.append(move)
                add = False
            if piece.color == 'white':
                list = self.get_all_moves(True, 'black')
            else:
                list = self.get_all_moves(True, 'white')

            for mov in list:
                if mov.capture and mov.capture.name == 'king':
                    if move in king_castling_moves:
                        king_castling_moves.remove(move)
                    add = False

            if add:
                good_move_list.append(move)

            self.unmake_move(move, piece, True)

        for mov in king_castling_moves:
            if self.allowing_castle(mov):
                good_move_list.append(mov)

        return good_move_list

    def attacking_king(self, color):
        if color == 'white':
            moves = self.white_moves
            king_in_check = 'black'
        else:
            moves = self.black_moves
            king_in_check = 'white'

        for mov in moves:
            if isinstance(mov.capture, King):
                self.in_check = king_in_check
                return

        self.in_check = 'None'

    def make_move(self, move, piece, testing=False):
        self.squares[move.initial_loc.location].piece = None
        self.squares[move.final_loc.location].piece = piece

        if piece.name == 'pawn':
            if abs(move.initial_loc.location - move.final_loc.location) == 16:
                piece.en_passant = True
            direction = piece.direction
            if self.last_move:
                if self.last_move.initial_loc.location == move.final_loc.location + direction:
                    if self.last_move.final_loc.location == move.final_loc.location-direction:
                        self.squares[move.final_loc.location -
                                     direction].piece = None
            if (move.final_loc.location < 8 or move.final_loc.location > 55):
                self.promoting_pawn = True
                self.promoting_pawn_color = piece.color
                self.promotion_square = self.squares[move.final_loc.location]

        if piece.name == 'king':
            if abs(move.initial_loc.location - move.final_loc.location) == 2:
                self.castle_rook_piece(move, piece)
        self.set_en_passant_false(move)
        if not testing:
            self.get_all_moves(None)

        self.attacking_king(piece.color)

    def unmake_move(self, move, piece, testing=False):
        self.squares[move.initial_loc.location].piece = piece
        if piece.name != 'pawn' or abs(move.initial_loc.location - move.final_loc.location) == 8:
            if move.capture:
                self.squares[move.final_loc.location].piece = move.capture
            else:
                self.squares[move.final_loc.location].piece = None
        else:
            if abs(move.initial_loc.location - move.final_loc.location) == 16:
                piece.en_passant = False
            if move.en_passant:
                direction = piece.direction
                if piece.color == 'white':
                    self.squares[move.final_loc.location -
                                 direction].piece = Pawn('black')
                else:
                    self.squares[move.final_loc.location -
                                 direction].piece = Pawn('white')
                self.squares[move.final_loc.location].piece = None
            else:
                self.squares[move.final_loc.location].piece = move.capture

        if piece.name == 'king':
            if self.squares[move.final_loc.location].piece and self.squares[move.final_loc.location].piece.name == 'king':
                self.squares[move.final_loc.location].piece = None
            if not self.squares[move.final_loc.location].piece:
                self.squares[move.initial_loc.location].piece = piece
            if abs(move.initial_loc.location - move.final_loc.location) == 2:
                final_location = move.final_loc.location
                if final_location == 2 or final_location == 58:
                    self.squares[final_location-2].piece = Rook(piece.color)
                    self.squares[final_location+1].piece = None
                elif final_location == 6 or final_location == 62:
                    self.squares[final_location+1].piece = Rook(piece.color)
                    self.squares[final_location-1].piece = None

        self.set_en_passant_false(move)
        if not testing:
            self.get_all_moves(None)

        self.attacking_king(piece.color)

    def castle_rook_piece(self, move, piece):
        final_location = move.final_loc.location
        if final_location == 2 or final_location == 58:
            self.squares[final_location-2].piece = None
            self.squares[final_location+1].piece = Rook(piece.color)
        elif final_location == 6 or final_location == 62:
            self.squares[final_location+1].piece = None
            self.squares[final_location-1].piece = Rook(piece.color)

    def render_pawn_promote(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render('Choose a piece to promote into', True, TEXT_COLOR)
        screen.blit(text, (815, 10))

        piece = Knight(self.promoting_pawn_color)
        piece.attach_texture_to_piece()
        img = pygame.image.load(piece.texture)
        img = pygame.transform.scale(img, (100, 100))
        screen.blit(img, (900, 50))

        piece = Bishop(self.promoting_pawn_color)
        piece.attach_texture_to_piece()
        img = pygame.image.load(piece.texture)
        img = pygame.transform.scale(img, (100, 100))
        screen.blit(img, (900, 150))

        piece = Rook(self.promoting_pawn_color)
        piece.attach_texture_to_piece()
        img = pygame.image.load(piece.texture)
        img = pygame.transform.scale(img, (100, 100))
        screen.blit(img, (1000, 50))

        piece = Queen(self.promoting_pawn_color)
        piece.attach_texture_to_piece()
        img = pygame.image.load(piece.texture)
        img = pygame.transform.scale(img, (100, 100))
        screen.blit(img, (1000, 150))

    def pawn_promote(self, location):
        if self.promotion_square == None:
            return
        piece = self.promotion_square.piece
        location_x, location_y = location
        if location_x > 900 and location_x < 1000:
            if location_y > 50 and location_y < 150:
                self.promotion_square.piece = Knight(piece.color)
                self.promoting_pawn = False
            elif location_y > 150 and location_y < 250:
                self.promotion_square.piece = Bishop(piece.color)
                self.promoting_pawn = False
        elif location_x > 1000 and location_x < 1100:
            if location_y > 50 and location_y < 150:
                self.promotion_square.piece = Rook(piece.color)
                self.promoting_pawn = False
            elif location_y > 150 and location_y < 250:
                self.promotion_square.piece = Queen(piece.color)
                self.promoting_pawn = False

        self.get_all_moves(None)

    def set_en_passant_false(self, move):
        for loc in range(0, 64):
            piece = self.squares[move.final_loc.location].piece
            secondPiece = self.squares[loc].piece
            if secondPiece and secondPiece.name == 'pawn' and piece != secondPiece:
                secondPiece.en_passant = False

    def get_all_moves(self, checking, checking_color=None):
        white_ar = []
        black_ar = []
        self.white_moves = white_ar
        self.black_moves = black_ar
        white_king = None
        black_king = None
        if not checking:
            checking = False
        for x in self.squares:
            if x.has_piece():
                piece = x.piece
                if not checking:
                    piece.clear_moves_list()
                if piece.name == 'king' and piece.color == 'white':
                    white_king = x.location
                elif piece.name == 'king':
                    black_king = x.location
                else:
                    match piece.name:
                        case 'pawn':
                            ar_two = self.pawn_moves(
                                x.location, piece)
                            if ar_two and piece.color == 'white':
                                white_ar.extend(ar_two)
                            elif ar_two and piece.color == 'black':
                                black_ar.extend(ar_two)
                        case 'queen':
                            ar_two = self.ranged_straight_moves(
                                x.location, piece, [7, 9, -7, -9, 8, -8, 1, -1])
                            if ar_two and piece.color == 'white':
                                white_ar.extend(ar_two)
                            elif ar_two and piece.color == 'black':
                                black_ar.extend(ar_two)
                        case 'rook':
                            ar_two = self.ranged_straight_moves(
                                x.location, piece, [1, -1, 8, -8])
                            if ar_two and piece.color == 'white':
                                white_ar.extend(ar_two)
                            elif ar_two and piece.color == 'black':
                                black_ar.extend(ar_two)
                        case 'bishop':
                            ar_two = self.ranged_straight_moves(
                                x.location, piece, [7, 9, -7, -9])
                            if ar_two and piece.color == 'white':
                                white_ar.extend(ar_two)
                            elif ar_two and piece.color == 'black':
                                black_ar.extend(ar_two)
                        case 'knight':
                            ar_two = self.knight_moves(x.location)
                            if ar_two and piece.color == 'white':
                                white_ar.extend(ar_two)
                            elif ar_two and piece.color == 'black':
                                black_ar.extend(ar_two)
                        case _:
                            pass
        white_king_moves = []
        black_king_moves = []

        if white_king:
            white_king_moves = self.king_moves(white_king)
        if black_king:
            black_king_moves = self.king_moves(black_king)
        if white_king_moves:
            white_ar.extend(white_king_moves)
        if black_king_moves:
            black_ar.extend(black_king_moves)
        self.generate_new_moves = False
        if checking and checking_color == 'white':

            return white_ar
        elif checking and checking_color == 'black':
            return black_ar
        if self.last_move and self.squares[self.last_move.final_loc.location].piece and self.squares[self.last_move.final_loc.location].piece.color == 'white':
            self.white_moves = self.check_for_checks(white_ar)
            self.black_moves = self.check_for_checks(black_ar)
            self.move_ordering()
        elif self.last_move:
            self.black_moves = self.check_for_checks(black_ar)
            self.white_moves = self.check_for_checks(white_ar)
            self.move_ordering()
        self.assign_to_piece()

    def assign_to_piece(self):
        for i in self.white_moves:
            piece = self.squares[i.initial_loc.location].piece
            piece.add_move(i)
        for i in self.black_moves:
            piece = self.squares[i.initial_loc.location].piece
            piece.add_move(i)

    def allowing_castle(self, move):
        if self.squares[move.initial_loc.location].piece.color == 'white':
            test_squares = [59, 60, 61]
            list = self.black_moves
        else:
            test_squares = [3, 4, 5]
            list = self.white_moves

        for i in test_squares:
            for mov in list:
                if mov.final_loc.location == i:
                    return False

        return True

    def king_moves(self, loc):
        if not self.squares[loc].piece:
            return
        checking_list = []

        square_direction = [loc-8, loc+8, loc+1,
                            loc-1, loc-9, loc-7, loc+7, loc+9]

        within_bounds = loc % 8

        for location in square_direction:
            if abs(location % 8 - within_bounds) > 1:
                pass
            elif not Square.out_of_range(location):
                square = self.squares[location]
                if square.has_enemy_or_empty(self.squares[loc].piece.color):
                    piece = square.piece
                    initial = Square(loc)
                    final = Square(location)
                    potential_move = Move(initial, final, piece)
                    checking_list.append(potential_move)

        if loc == 60 or loc == 4:
            if self.squares[loc+1].is_empty() and self.squares[loc+2].is_empty() and self.squares[loc+3].piece and self.squares[loc+3].piece.name == 'rook':
                if not self.squares[loc].piece.moved_from_start and not self.squares[loc+3].piece.moved_from_start:
                    initial = Square(loc)
                    final = Square(loc+2)
                    potential_move = Move(initial, final)
                    checking_list.append(potential_move)

        if loc == 60 or loc == 4:
            if self.squares[loc-1].is_empty() and self.squares[loc-2].is_empty() and self.squares[loc-3].is_empty() and self.squares[loc-4].piece and self.squares[loc-4].piece.name == 'rook':
                if not self.squares[loc].piece.moved_from_start and not self.squares[loc-4].piece.moved_from_start:
                    initial = Square(loc)
                    final = Square(loc-2)
                    potential_move = Move(initial, final)
                    checking_list.append(potential_move)

        return checking_list

    def pawn_moves(self, loc, piece):
        if piece.moved_from_start:
            max_step = 1
        else:
            max_step = 2
        checking_list = []
        dir = piece.direction
        if not Square.out_of_range(loc+dir):
            if self.squares[loc+dir].is_empty():
                initial = Square(loc)
                final = Square(loc+dir)
                move = Move(initial, final)
                checking_list.append(move)

                dir = dir + piece.direction
                if max_step == 2 and not Square.out_of_range(loc+dir):
                    if self.squares[loc+dir].is_empty():
                        initial = Square(loc)
                        final = Square(loc+dir)
                        move = Move(initial, final)
                        checking_list.append(move)

        interval_one = None
        interval_two = None

        if loc > 23 and loc < 32:
            interval_one = -7
            interval_two = -9
        elif loc > 31 and loc < 40:
            interval_one = 9
            interval_two = 7

        if interval_two and (loc % 8 != 0) and not Square.out_of_range(loc-1):
            if self.squares[loc-1].has_enemy_piece(piece.color):
                piece2 = self.squares[loc-1].piece
                if piece2 != None and piece2.name == 'pawn' and piece2.en_passant:
                    initial = Square(loc)
                    final = Square(loc+interval_two)
                    move = Move(initial, final, piece2, True)
                    checking_list.append(move)

        if interval_one and (loc % 8 != 7) and not Square.out_of_range(loc+1):
            if self.squares[loc+1].has_enemy_piece(piece.color):
                piece2 = self.squares[loc+1].piece
                if piece2 != None and piece2.name == 'pawn' and piece2.en_passant:
                    initial = Square(loc)
                    final = Square(loc+interval_one)
                    move = Move(initial, final, piece2, True)
                    checking_list.append(move)

        potential_loc = loc + piece.direction
        if (loc % 8 != 0) and not Square.out_of_range(potential_loc-1) and self.squares[potential_loc-1].has_enemy_piece(piece.color):
            initial = Square(loc)
            final = Square(potential_loc-1)
            move = Move(initial, final,
                        self.squares[potential_loc-1].piece)
            checking_list.append(move)

        if (loc % 8 != 7) and not Square.out_of_range(potential_loc+1) and self.squares[potential_loc+1].has_enemy_piece(piece.color):
            initial = Square(loc)
            final = Square(potential_loc+1)
            move = Move(initial, final, self.squares[potential_loc+1].piece)
            checking_list.append(move)

        return checking_list

    def ranged_straight_moves(self, loc, piece, arr):
        checking_list = []
        for i in arr:
            potential_loc = loc
            while True:
                temp = potential_loc + i
                temp2 = abs((temp % 8) - (potential_loc % 8))
                if temp2 > 1:
                    break
                else:
                    potential_loc = temp
                if not Square.out_of_range(potential_loc):
                    initial = Square(loc)
                    final = Square(potential_loc)
                    move = Move(
                        initial, final, self.squares[potential_loc].piece)
                    if self.squares[potential_loc].is_empty():
                        checking_list.append(move)
                    elif self.squares[potential_loc].has_enemy_piece(piece.color):
                        checking_list.append(move)
                        break
                    elif not self.squares[potential_loc].has_enemy_or_empty(piece.color):
                        break
                else:
                    break
        return checking_list

    def knight_moves(self, loc):
        checking_list = []
        piece = self.squares[loc].piece
        possible_moves = [loc-10, loc-17, loc-15,
                          loc-6, loc+6, loc+10, loc+15, loc+17]

        within_bounds = loc % 8

        for possible_move_loc in possible_moves:
            if abs(possible_move_loc % 8 - within_bounds) > 2:
                pass
            elif not Square.out_of_range(possible_move_loc):
                if self.squares[possible_move_loc].has_enemy_or_empty(piece.color):
                    initial = Square(loc)
                    final_piece = self.squares[possible_move_loc].piece
                    final = Square(possible_move_loc)
                    move = Move(initial, final, final_piece)

                    checking_list.append(move)

        return checking_list

    def move_is_valid(self, piece, move):
        return move in piece.moves

    def evaluate_board(self, color):
        white_value = 0
        black_value = 0
        for i in range(0, 64):
            piece = self.squares[i].piece
            if piece:
                if piece.color == 'white':
                    white = True
                else:
                    white = False
                match piece.name:
                    case 'king':
                        if white:
                            white_value += piece.value + white_king_table[i]
                        else:
                            black_value += piece.value + black_king_table[i]
                    case 'pawn':
                        if white:
                            white_value += piece.value + white_pawn_table[i]
                        else:
                            black_value += piece.value + black_pawn_table[i]
                    case 'bishop':
                        if white:
                            white_value += piece.value + white_bishop_table[i]
                        else:
                            black_value += piece.value + black_bishop_table[i]
                    case 'knight':
                        if white:
                            white_value += piece.value + white_knight_table[i]
                        else:
                            black_value += piece.value + black_knight_table[i]
                    case 'rook':
                        if white:
                            white_value += piece.value + white_rook_table[i]
                        else:
                            black_value += piece.value + black_rook_table[i]
                    case 'queen':
                        if white:
                            white_value += piece.value + white_queen_table[i]
                        else:
                            black_value += piece.value + black_queen_table[i]
                    case _:
                        pass

        if color == 'white':
            return white_value - black_value
        else:
            return black_value - white_value

    def move_ordering(self):
        self.white_moves.sort(key=lambda x: x.capture_worth, reverse=True)
        self.black_moves.sort(key=lambda x: x.capture_worth, reverse=True)


'''
    def __put_start_pieces_in_location(self):
        self.fen_to_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')'''


white_pawn_table = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5, -10,  0,  0, -10, -5,  5,
    5, 10, 10, -20, -20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
])

white_knight_table = np.array([
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
])

white_bishop_table = np.array([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0, 10, 10, 10, 10,  0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
])

white_rook_table = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
])

white_queen_table = np.array([
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0, -10,
    -10,  0,  5,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
])


white_king_table = np.array([
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    0,  0,  0,  0,  0,  0,  0,  0,
    20, 30, 10,  0,  0, 10, 30, 20
])

# switch to black

black_pawn_table = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0
])

black_knight_table = np.array([
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
])

black_bishop_table = np.array([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10, 10, 10, 10, 10, 10,  10, -10,
    -10,  0, 10, 10, 10,  10,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
])

black_rook_table = np.array([
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0,  -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5,  10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
])

black_queen_table = np.array([
    -20, -10, -10, -5, -5, -10, -10, -20,
    - 10,  0,  5,  0,  0,  0,  0, -10,
    -10,  5,  5,  5,  5,  5,  0, -10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
])


black_king_table = np.array([
    20, 30, 10,  0,  0, 10, 30, 20,
    0,  0,  0,  0,  0,  0,  0,  0,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
])
