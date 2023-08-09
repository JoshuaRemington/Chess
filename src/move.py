import numpy as np


class Move():

    def __init__(self, initial, final, capture=None, en_passant=None):
        self.initial_loc = initial
        self.final_loc = final
        self.capture = capture
        self.en_passant = en_passant
        self.capture_worth = 0
        self.get_capture_worth()

    def get_capture_worth(self):
        if not self.capture:
            return
        else:
            piece = self.capture
        if piece.color == 'white':
            match piece.name:
                case 'pawn':
                    self.capture_worth = 100 + \
                        white_pawn_table[self.final_loc.location]
                case 'bishop':
                    self.capture_worth = 330 + \
                        white_bishop_table[self.final_loc.location]
                case 'knight':
                    self.capture_worth = 320 + \
                        white_knight_table[self.final_loc.location]
                case 'rook':
                    self.capture_worth = 500 + \
                        white_rook_table[self.final_loc.location]
                case 'queen':
                    self.capture_worth = 900 + \
                        white_queen_table[self.final_loc.location]
                case 'king':
                    self.capture_worth = 20000.0 + \
                        white_king_table[self.final_loc.location]
                case _:
                    pass

        if piece.color == 'black':
            match piece.name:
                case 'pawn':
                    self.capture_worth = 100 + \
                        black_pawn_table[self.final_loc.location]
                case 'bishop':
                    self.capture_worth = 330 + \
                        black_bishop_table[self.final_loc.location]
                case 'knight':
                    self.capture_worth = 320 + \
                        black_knight_table[self.final_loc.location]
                case 'rook':
                    self.capture_worth = 500 + \
                        black_rook_table[self.final_loc.location]
                case 'queen':
                    self.capture_worth = 900 + \
                        black_queen_table[self.final_loc.location]
                case 'king':
                    self.capture_worth = 20000.0 + \
                        black_king_table[self.final_loc.location]
                case _:
                    pass

    def __eq__(self, other):
        if self.initial_loc.location != other.initial_loc.location:
            return False
        if self.final_loc.location != other.final_loc.location:
            return False

        return True


white_pawn_table = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5, -10,  0,  0, -10, -5,  5,
    5, 10, 10, -20, -20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0,
])

white_knight_table = np.array([
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
])

white_bishop_table = np.array([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0, 10, 10, 10, 10,  0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
])

white_rook_table = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0,
])

white_queen_table = np.array([
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0, -10,
    -10,  0,  5,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
])


white_king_table = np.array([
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    0,  0,  0,  0,  0,  0,  0,  0,
    20, 30, 10,  0,  0, 10, 30, 20,
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
    0,  0,  0,  0,  0,  0,  0,  0,
])

black_knight_table = np.array([
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
])

black_bishop_table = np.array([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10, 10, 10, 10, 10, 10,  10, -10,
    -10,  0, 10, 10, 10,  10,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
])

black_rook_table = np.array([
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0,  -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5,  10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0,
])

black_queen_table = np.array([
    -20, -10, -10, -5, -5, -10, -10, -20,
    - 10,  0,  5,  0,  0,  0,  0, -10,
    -10,  5,  5,  5,  5,  5,  0, -10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
])


black_king_table = np.array([
    20, 30, 10,  0,  0, 10, 30, 20,
    0,  0,  0,  0,  0,  0,  0,  0,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
])
