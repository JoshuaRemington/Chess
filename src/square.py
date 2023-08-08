

class Square():

    def __init__(self, location, piece=None):
        self.location = location
        self.piece = piece
        self.attacked = False

    def has_piece(self):
        return self.piece != None

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def has_enemy_or_empty(self, color):
        return self.has_enemy_piece(color) or self.is_empty()

    def is_empty(self):
        return not self.has_piece()

    @staticmethod
    def out_of_range(*args):
        for arg in args:
            if arg < 0 or arg > 63:
                return True

        return False
