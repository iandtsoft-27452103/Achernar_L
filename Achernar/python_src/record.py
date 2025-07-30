#import board
#import result

class record:
    def __init__(self, r):
        self.black_player = ""
        self.white_player = ""
        self.result = r.black_win
        #self.str_moves = [] * (b.square_nb + 100)
        #self.moves = [] * (b.square_nb + 100)
        self.str_moves = []
        self.moves = []
        self.ply = 1