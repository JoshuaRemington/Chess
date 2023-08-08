

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
        match self.capture.name:
            case 'pawn':
                self.capture_worth = 1
            case 'bishop':
                self.capture_worth = 3
            case 'knight':
                self.capture_worth = 3
            case 'rook':
                self.capture_worth = 5
            case 'queen':
                self.capture_worth = 9
            case 'king':
                self.capture_worth = 900
            case _:
                pass

    def __eq__(self, other):
        if self.initial_loc.location != other.initial_loc.location:
            return False
        if self.final_loc.location != other.final_loc.location:
            return False

        return True
