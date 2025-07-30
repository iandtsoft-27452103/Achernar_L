class makemove:
    #plyは要らないか？
    def makemove(self, bo, sq, color, ply, f, r, bi, st):
        add_dame_count = 0
        count = 0
        m = 0
        v1 = [0, 0, 0, 0]
        v2 = [0, 0, 0, 0]
        v3 = [0, 0, 0, 0]
        v4 = [0, 0, 0, 0]
        bo.bb_color[color] = bi.xor(sq, bo.bb_color[color])
        bo.bb_occupied = bi.xor(sq, bo.bb_occupied)
        bo.board[sq] = color
        bb_cross = bi.bb_kou_hantei_table[sq]
        bb = bi.bb_and(bo.bb_color[color], bb_cross)

        if bb == 0:
            #自分の石と連絡していない手
            bo.seq_number_table[color][sq] = bo.seq_num[color]
            bo.bb_seq[color][bo.seq_num[color]] = bi.xor(sq, bo.bb_seq[color][bo.seq_num[color]])
            bb = bo.bb_dame[color][bo.seq_num[color]] = bi.bb_not_and(bb_cross, bo.bb_occupied)
            bo.seq_num[color] += 1
            #bb = bi.bb_not_and(bb_cross, bo.bb_occupied)
            add_dame_count = bi.popu_count(bb)
            #isq = bi.first_one(bb)
            v1[0] = sq
            v2[0] = bo.seq_number_table[color][sq]
            m += 1
        else:
            #自分の石と連絡している手
            while bb != 0:
                isq = bi.first_one(bb)
                bb = bi.xor(isq, bb)
                v1[count] = isq
                v2[count] = bo.seq_number_table[color][isq]
                count += 1
                m += 1

            base_number = v2[0]
            bo.seq_number_table[color][sq] = base_number
            bo.bb_seq[color][base_number] = bi.xor(sq, bo.bb_seq[color][base_number])
            bb = bi.bb_not_and(bb_cross, bo.bb_occupied)
            add_dame_count = bi.popu_count(bb)
            bo.bb_dame[color][base_number] = bi.bb_or(bo.bb_dame[color][base_number], bb)
            #bo.bb_dame[color][base_number] = bi.xor(sq, bo.bb_dame[color][base_number])

            for i in range(1, count):
                bo.bb_seq[color][v2[i]] = bi.xor(sq, bo.bb_seq[color][v2[i]])
                bo.bb_seq[color][base_number] = bi.bb_or(bo.bb_seq[color][base_number], bo.bb_seq[color][v2[i]])
                bo.bb_dame[color][base_number] = bi.bb_or(bo.bb_dame[color][base_number], bo.bb_dame[color][v2[i]])
                #bo.bb_dame[color][base_number] = bi.xor(sq, bo.bb_dame[color][base_number])

                #連番号を書き換える
                bb = bo.bb_seq[color][v2[i]]
                while bb != 0:
                    isq = bi.first_one(bb)
                    bb = bi.xor(isq, bb)
                    bo.seq_number_table[color][isq] = base_number

                bo.bb_seq[color][v2[i]] = bi.bb_ini()
                bo.bb_dame[color][v2[i]] = bi.bb_ini()
            bo.bb_dame[color][base_number] = bi.xor(sq, bo.bb_dame[color][base_number])

        #4つの連をツグ手の場合、相手の駄目を詰めないので終了
        if count == 4:
            return
        #自分の石と連絡せず、相手の駄目も詰めない手の場合終了
        if add_dame_count == 4:
            return
        if sq == 0 or sq == 18 or sq == 342 or sq == 360:
            if add_dame_count == 2:
                return
        if sq != 0 and sq != 18 and sq != 342 and sq != 360:
            if bo.file_table[sq] == f.file1 or bo.file_table[sq] == f.file19:
                if add_dame_count == 3:
                    return
            if bo.rank_table[sq] == r.rank1 or bo.rank_table[sq] == r.rank19:
                if add_dame_count == 3:
                    return
        #count2 = 0
        x = 0

        bb = bi.bb_and(bo.bb_color[color ^ 1], bb_cross)
        
        while bb != 0:
            isq = bi.first_one(bb)
            bb = bi.xor(isq, bb)
            v3[x] = bo.seq_number_table[color ^ 1][isq]
            x += 1

        for i in range(x):
            bb_dame = bi.bb_and(bi.bb_mask[sq], bo.bb_dame[color ^ 1][v3[i]])
            if bb_dame != 0:
                #count2 += 1
                bo.bb_dame[color ^ 1][v3[i]] = bi.bb_not_and(bo.bb_dame[color ^ 1][v3[i]], bb_dame)
                j = bi.popu_count(bo.bb_dame[color ^ 1][v3[i]])
                #トリの手の場合
                if j == 0:
                    bb = bo.bb_seq[color ^ 1][v3[i]]
                    k = bi.popu_count(bb)
                    bo.agehama[color] += k
                    while bb != 0:
                        isq = bi.first_one(bb)
                        bb = bi.xor(isq, bb)
                        bo.bb_color[color ^ 1] = bi.xor(isq, bo.bb_color[color ^ 1])
                        bo.bb_occupied = bi.xor(isq, bo.bb_occupied)
                        bo.board[isq] = st.blank
                        for k in range(m):
                            bb2 = bi.bb_and(bi.bb_kou_hantei_table[isq], bo.bb_seq[color][v2[k]])
                            if bb2 != 0:
                                bo.bb_dame[color][v2[k]] = bi.bb_or(bo.bb_dame[color][v2[k]], bi.bb_mask[isq])
                        y = 0
                        bb2 = bi.bb_and(bo.bb_color[color], bi.bb_kou_hantei_table[isq])
                        while bb2 != 0:
                            isq2 = bi.first_one(bb2)
                            bb2 = bi.xor(isq2, bb2)
                            v4[y] = bo.seq_number_table[color][isq2]
                            y += 1
                        for k in range(y):
                            bb2 = bi.bb_and(bi.bb_kou_hantei_table[isq], bo.bb_seq[color][v4[k]])
                            if bb2 != 0:
                                bo.bb_dame[color][v4[k]] = bi.bb_or(bo.bb_dame[color][v4[k]], bi.bb_mask[isq])

                    #所属する連番号を初期化する
                    bb = bo.bb_seq[color ^ 1][v3[i]]
                    while bb != 0:
                        isq = bi.first_one(bb)
                        bb = bi.xor(isq, bb)
                        bo.seq_number_table[color ^ 1][isq] = bo.seq_max

                    bo.bb_seq[color ^ 1][v3[i]] = bi.bb_ini()

    #探索用
    def makemove_search(self, bo, sq, color, ply, f, r, bi, st):
        add_dame_count = 0
        count = 0
        bo.bb_color[color] = bi.xor(sq, bo.bb_color[color])
        bo.bb_occupied = bi.xor(sq, bo.bb_occupied)
        bo.board[sq] = color
        #2021.06.23 Add Start
        bo.saved_hash_key[ply] = bo.hash_key
        bo.hash_key ^= bo.hash[color][sq]
        bo.saved_agehama[color][ply] = bo.agehama[color]
        #2021.06.23 Add End
        bb_cross = bi.bb_kou_hantei_table[sq]
        bb = bi.bb_and(bo.bb_color[color], bb_cross)

        if bb == 0:
            #自分の石と連絡していない手
            #2021.06.23 Add Start
            bo.connect_flag[ply] = 0
            #2021.06.23 Add End
            bo.bb_seq[color][bo.seq_num[color]] = bi.xor(sq, bo.bb_seq[color][bo.seq_num[color]])
            bo.bb_dame[color][bo.seq_num[color]] = bi.bb_not_and(bb_cross, bo.bb_occupied)
            bo.seq_num[color] += 1
            bb = bi.bb_not_and(bb_cross, bo.bb_occupied)
            add_dame_count = bi.popu_count(bb)
        else:
            #自分の石と連絡している手
            #2021.06.23 Add Start
            bo.connect_flag[ply] = 1
            #2021.06.23 Add End
            for i in range(bo.seq_max):
                if i == bo.seq_num[color] or count == 4:
                    break
                bb = bi.bb_and(bo.bb_seq[color][i], bb_cross)
                if bb == 0:
                    continue
                else:
                    #ツグ手の場合
                    if count == 0:
                        #2021.06.23 Add Start
                        bo.saved_base_seq_num[ply] = i
                        bo.saved_base_seq_bb[ply] = bo.bb_seq[color][i]
                        bo.saved_base_dame_bb[ply] = bo.bb_dame[color][i]
                        #2021.06.23 Add End
                        bo.bb_seq[color][i] = bi.xor(sq, bo.bb_seq[color][i])
                        bb = bi.bb_not_and(bb_cross, bo.bb_occupied)
                        add_dame_count = bi.popu_count(bb)
                        bo.bb_dame[color][i] = bi.bb_or(bo.bb_dame[color][i], bb)
                        bo.bb_dame[color][i] = bi.xor(sq, bo.bb_dame[color][i])
                        base_number = i
                    else:
                        #2021.06.23 Add Start
                        bo.saved_seq_num[ply][count - 1] = i
                        bo.saved_seq_bb[ply][count - 1] = bo.bb_seq[color][i]
                        bo.saved_dame_bb[ply][count - 1] = bo.bb_dame[color][i]
                        #2021.06.23 Add End
                        bo.bb_seq[color][i] = bi.xor(sq, bo.bb_seq[color][i])
                        bo.bb_seq[color][base_number] = bi.bb_or(bo.bb_seq[color][base_number], bo.bb_seq[color][i])
                        bo.bb_dame[color][base_number] = bi.bb_or(bo.bb_dame[color][base_number], bo.bb_dame[color][i])
                        bo.bb_dame[color][base_number] = bi.xor(sq, bo.bb_dame[color][base_number])
                        bo.bb_seq[color][i] = bi.bb_ini()
                        bo.bb_dame[color][i] = bi.bb_ini()
                    count += 1
        #4つの連をツグ手の場合、相手の駄目を詰めないので終了
        if count == 4:
            return
        #自分の石と連絡せず、相手の駄目も詰めない手の場合終了
        if add_dame_count == 4:
            return
        if sq == 0 or sq == 18 or sq == 342 or sq == 360:
            if add_dame_count == 2:
                return
        if sq != 0 and sq != 18 and sq != 342 and sq != 360:
            if bo.file_table[sq] == f.file1 or bo.file_table[sq] == f.file19:
                if add_dame_count == 3:
                    return
            if bo.rank_table[sq] == r.rank1 or bo.rank_table[sq] == r.rank19:
                if add_dame_count == 3:
                    return
        count = 0
        #2021.06.23 Add Start
        tori_cnt = 0
        l = 0
        #2021.06.23 Add End
        for i in range(bo.seq_max):
            if i == bo.seq_num[color ^ 1]:
                break
            j = bi.popu_count(bo.bb_dame[color ^ 1][i])
            #抜け番号の場合continueする
            if j == 0:
                continue
            bb_dame = bi.bb_and(bi.bb_mask[sq], bo.bb_dame[color ^ 1][i])
            if bb_dame != 0:
                #2021.06.23 Add Start
                bo.saved_opp_seq_num[ply][count] = i
                bo.saved_opp_dame_bb[ply][count] = bo.bb_dame[color ^ 1][i]
                #2021.06.23 Add End
                count += 1
                bo.bb_dame[color ^ 1][i] = bi.bb_not_and(bo.bb_dame[color ^ 1][i], bb_dame)
                j = bi.popu_count(bo.bb_dame[color ^ 1][i])
                #トリの手の場合
                if j == 0:
                    bb = bo.bb_seq[color ^ 1][i]
                    k = bi.popu_count(bb)
                    #2021.06.23 Add Start
                    bo.tori_flag[ply] = 1
                    #2021.06.23 Add End
                    bo.agehama[color] += k
                    #2021.06.23 Add Start
                    bo.saved_agehama[color][ply] = bo.agehama[color]
                    #2021.06.23 Add End
                    while bb != 0:
                        isq = bi.first_one(bb)
                        bb = bi.xor(isq, bb)
                        bo.bb_color[color ^ 1] = bi.xor(isq, bo.bb_color[color ^ 1])
                        bo.bb_occupied = bi.xor(isq, bo.bb_occupied)
                        bo.board[isq] = st.blank
                        #2021.06.23 Add Start
                        bo.saved_made_dame_square[ply][l] = isq
                        l += 1
                        #2021.06.23 Add End
                        for k in range(bo.seq_max):
                            if k == bo.seq_num[color]:
                                break
                            bb2 = bi.bb_and(bi.bb_kou_hantei_table[isq], bo.bb_seq[color][k])
                            if bb2 != 0:
                                bo.bb_dame[color][k] = bi.bb_or(bo.bb_dame[color][k], bi.bb_mask[isq])
                    #取った連番号とビットボードを保存する
                    #2021.06.23 Add Start
                    bo.removed_seq_num[ply][tori_cnt] = i
                    bo.removed_seq_bb[ply][tori_cnt] = bo.bb_seq[color ^ 1][i]
                    tori_cnt += 1
                    #2021.06.23 Add End
                    #2021.06.23 Delete Start
                    #bo.bb_seq[color ^ 1][i] = bi.bb_ini()
                    #2021.06.23 Delete End
                    #2021.06.23 Add Start
                    while bo.bb_seq[color ^ 1][i] != 0:
                        isq = bi.first_one(bo.bb_seq[color ^ 1][i])
                        bo.bb_seq[color ^ 1][i] = bi.xor(isq, bo.bb_seq[color ^ 1][i])
                        bo.hash_key ^= bo.hash[color ^ 1][isq]
                    #2021.06.23 Add End