import board
class position:
    def __init__(self):
        self.posi_no = 0
        self.record_no = 0
        self.ply = 0

    def number_position(self, rec):
        positions = []

        posi_cnt = 0
        for i in range(len(rec)):
            bo = board.board()
            pos = position()
            pos.posi_no = posi_cnt
            pos.record_no = i
            pos.ply = 0
            positions.append(pos)
            posi_cnt += 1
            for j in range(1, len(rec[i].moves)):
                pos = position()
                pos.posi_no = posi_cnt
                pos.record_no = i
                pos.ply = j
                positions.append(pos)
                posi_cnt += 1

        return positions