class unmakemove:
#    def unmakemove(self, bo, sq, color, ply, f, r, bi, st):
#※ 高速化の修正はしていない
    def unmakemove(self, bo, sq, color, ply, bi, st):
        cnt = 0
        bo.bb_color[color] = bi.xor(sq, bo.bb_color[color])
        bo.bb_occupied = bi.xor(sq, bo.bb_occupied)
        bo.board[sq] = st.blank
        bo.hash_key = bo.saved_hash_key[ply]
        bo.agehama[color] = bo.saved_agehama[color][ply]

        if bo.connect_flag[ply] == 0:
            #自分の石と連絡していない手の場合
            bo.bb_seq[color][bo.seq_num[color] - 1] = bi.bb_ini()
            bo.bb_dame[color][bo.seq_num[color] - 1] = bi.bb_ini()
            bo.seq_num[color] -= 1
        else:
            #自分の石と連絡している場合の手（ノビ, サガリ, ツギ他）

            #基になる連番号の情報を戻す
            bo.bb_seq[color][bo.saved_base_seq_num[ply]] = bo.saved_base_seq_bb[ply]
            bo.bb_dame[color][bo.saved_base_seq_num[ply]] = bo.saved_base_dame_bb[ply]
            bo.connect_flag[ply] = 0
            bo.saved_base_seq_num[ply] = bo.seq_max
            bo.saved_base_seq_bb[ply] = bi.bb_ini()
            bo.saved_base_dame_bb[ply] = bi.bb_ini()

            #ツイだ連番号の情報を戻す
            for i in range(3):
                if bo.saved_seq_num[ply][i] == bo.seq_max:
                    break
                bo.bb_seq[color][bo.saved_seq_num[ply][i]] = bo.saved_seq_bb[ply][i]
                bo.bb_dame[color][bo.saved_seq_num[ply][i]] = bo.saved_dame_bb[ply][i]
                bo.saved_seq_num[ply][i] = bo.seq_max
                bo.saved_seq_bb[ply][i] = bi.bb_ini()
                bo.saved_dame_bb[ply][i] = bi.bb_ini()

        for i in range(4):
            if bo.saved_opp_seq_num[ply][i] == bo.seq_max:
                break
            #相手の連の詰めた駄目を戻す
            bo.bb_dame[color ^ 1][bo.saved_opp_seq_num[ply][i]] = bo.saved_opp_dame_bb[ply][i]
            bo.saved_opp_seq_num[ply][i] = bo.seq_max
            bo.saved_opp_dame_bb[ply][i] = bi.bb_ini()

        if bo.tori_flag[ply] == 1:
            #トリの手だった場合
            for i in range(4):
                if bo.removed_seq_num[ply][i] == bo.seq_max:
                    break
                bo.bb_seq[color ^ 1][bo.removed_seq_num[ply][i]] = bo.removed_seq_bb[ply][i]
                cnt = bi.popu_count(bo.removed_seq_bb[ply][i])
                bo.agehama[color] -= cnt

                bb = bo.removed_seq_bb[ply][i]
                while bb != 0:
                    isq = bi.first_one(bb)
                    bb = bi.xor(isq, bb)
                    bo.bb_color[color ^ 1] = bi.xor(isq, bo.bb_color[color ^ 1])
                    bo.bb_occupied = bi.xor(isq, bo.bb_occupied)
                    bo.board[isq] = color ^ 1
                bo.removed_seq_num[ply][i] = bo.seq_max
                bo.removed_seq_bb[ply][i] = bi.bb_ini()

            for i in range(128):
                if bo.saved_made_dame_square[ply][i] == bo.square_nb:
                    break
                for j in range(bo.seq_max):
                    if j == bo.seq_num[color]:
                        break
                    isq = bo.saved_made_dame_square[ply][i]
                    bb = bi.bb_and(bo.bb_dame[color][j], bi.bb_mask[isq])

                    if bb != 0:
                        bo.bb_dame[color][j] = bi.xor(isq, bb)
                bo.saved_made_dame_square[ply][i] = bo.square_nb

            bo.kou_array[ply] = bo.square_nb
            bo.tori_flag[ply] = 0