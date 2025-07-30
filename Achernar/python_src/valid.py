class valid:
    def __init__(self):
        self.color = 0

    #自殺手かどうかのチェックに使う
    def is_kou(self, bo, bi, move):
        bb1 = bi.bb_kou_hantei_table[move]
        i = bi.popu_count(bb1)
        bb2 = bi.bb_and(bb1, bo.bb_color[self.color])
        j = bi.popu_count(bb2)
        if i != j + 1:
            return 0
        else:
            return 1

    #合法手かどうか調べる
    def is_move_valid(self, bo, bi, move, st):
        flag = 0
        for i in range(bo.seq_max):
            if i == bo.seq_num[self.color]:
                break
            bb1 = bo.bb_dame[self.color][i]
            count = bi.popu_count(bb1)
            bb2 = bi.bb_and(bb1, bi.bb_mask[move])
            if bb2 != 0:
                if count >= 2:
                    #自分の駄目を埋める手かつ駄目の数が2以上だったら合法手
                    return 0
                elif count == 1:
                    bb3 = bi.bb_kou_hantei_table[move]
                    while bb3 != 0:
                        sq = bi.first_one(bb3)
                        bb3 = bi.xor(sq, bb3)
                        if bo.board == st.blank:
                            #駄目が増えるので合法手
                            return 0
                    #1つの駄目を埋める手なので非合法手候補
                    flag = 1
        bb1 = bi.bb_kou_hantei_table[move]
        count = bi.popu_count(bb1)
        bb2 = bi.bb_and(bb1, bo.bb_color[self.color ^ 1])
        count2 = bi.popu_count(bb2)
        if count == count2:
            if self.is_kou(bo, bi,move) == 0:
                #相手の一眼を埋める手→自殺手
                return 0

        #新しく連を作る手なので合法手
        if flag == 0:
            return 0

        return 1


