import torch
import torch.nn as nn
import torchvision
import torch.functional as F
import policy
import policy_conv3d
import policy_lazy
import file
import rank
import bitop
import stone
import makemove
import feature
import record
import result
import numpy

class think:
    def __init__(self):
        self.color = 0
        self.ply = 1
        self.str_file = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T']
        self.str_rank = ['19','18','17','16','15','14','13','12','11','10','9','8','7','6','5','4','3','2','1']
        self.f = file.file()
        self.r = rank.rank()
        self.st = stone.stone()
        self.res = result.result()
        self.rec = record.record(self.res)
        self.model = policy_lazy.policy()
        self.model.load_state_dict(torch.load('model.pth'))

    #思考する
    def think(self, bo, bi, ft):
        ma = makemove.makemove()

        device = torch.device("cuda:0")
        self.model = self.model.to(device)

        li = []
        fe = ft.make_input_features(bo, self.color, self.rec, self.ply - 1)
        li.append(fe)

        li = numpy.array(li)

        self.model.eval()

        with torch.no_grad():
            x = torch.tensor(li, dtype = torch.float)
            x = x.to(device)
            y = self.model(x)
            y = y.to("cpu")
            z = y.data[0].tolist()

            #li2 = []
            #for i in range(19):
                #for j in range(19):
                    #li2.append(z[1][i][j])

            bb_full = (1 << 361) - 1
            cnt = bi.popu_count(bb_full)
            bb_move = bi.bb_not_and(bb_full, bo.bb_occupied)

            move = []
            while bb_move != 0:
                sq = bi.first_one(bb_move)
                bb_move = bi.xor(sq, bb_move)
                #コウでない
                if sq != bo.kou:
                    #合法手である
                    if self.is_move_valid(bo, bi, sq, self.st) == 0:
                        move.append(sq)
            bestscore = 0
            first = 0
            for i in range(19):
                for j in range(19):
                    cur_move = (j * bo.nrank) + i
                    cur = z[1][cur_move]
                    flag = 0
                    for k in range(len(move)):
                        if cur_move == move[k]:
                            flag = 1
                    if flag == 0:
                        continue;
                    if first == 0:
                        best_sq = j * bo.nrank + i
                        bestscore = z[1][best_sq]
                        bestmove = self.board_to_gtp(i, j)
                        first = 1
                        continue;
                    if cur > bestscore:
                        best_sq = j * bo.nrank + i
                        bestscore = z[1][best_sq]
                        bestmove = self.board_to_gtp(i, j)
        
        if bestscore < 0.2 and self.ply >= 240:
            return 'resign'
        elif bestscore > 0.60 and self.ply >= 300:
            return 'PASS'

        ma.makemove(bo, best_sq, self.color, self.ply, self.f, self.r, bi, self.st)
        self.rec.moves.append(best_sq)
        self.ply += 1
        return bestmove
    
    #コウのマスをセットする
    def set_kou(self, bo, bi, move):
        bb1 = bi.bb_kou_hantei_table[move]
        i = bi.popu_count(bb1)
        bb2 = bi.bb_and(bb1, bo.bb_color[self.color ^ 1])
        j = bi.popu_count(bb2)
        if i != j + 1:
            bo.kou = bo.square_nb
            return
        bb3 = bi.bb_not_and(bb1, bb2)
        isq = bi.first_one(bb3)
        bo.kou = isq

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

    #GTPに変換する
    def board_to_gtp(self, ifile, irank):
        str_move = self.str_file[ifile] + self.str_rank[irank]
        return str_move

    #盤面に変換する
    def gtp_to_board(self, bo, bi, str_move):
        ma = makemove.makemove()
        l = len(str_move)
        irank = 0
        ifile = 0

        if str_move[0] == 'A':
            ifile = self.f.file1
        elif str_move[0] == 'B':
            ifile = self.f.file2
        elif str_move[0] == 'C':
            ifile = self.f.file3
        elif str_move[0] == 'D':
            ifile = self.f.file4
        elif str_move[0] == 'E':
            ifile = self.f.file5
        elif str_move[0] == 'F':
            ifile = self.f.file6
        elif str_move[0] == 'G':
            ifile = self.f.file7
        elif str_move[0] == 'H':
            ifile = self.f.file8
        elif str_move[0] == 'J':
            ifile = self.f.file9
        elif str_move[0] == 'K':
            ifile = self.f.file10
        elif str_move[0] == 'L':
            ifile = self.f.file11
        elif str_move[0] == 'M':
            ifile = self.f.file12
        elif str_move[0] == 'N':
            ifile = self.f.file13
        elif str_move[0] == 'O':
            ifile = self.f.file14
        elif str_move[0] == 'P':
            ifile = self.f.file15
        elif str_move[0] == 'Q':
            ifile = self.f.file16
        elif str_move[0] == 'R':
            ifile = self.f.file17
        elif str_move[0] == 'S':
            ifile = self.f.file18
        elif str_move[0] == 'T':
            ifile = self.f.file19

        if l == 2:
            if str_move[1] == '1':
                irank = self.r.rank19
            elif str_move[1] == '2':
                irank = self.r.rank18
            elif str_move[1] == '3':
                irank = self.r.rank17
            elif str_move[1] == '4':
                irank = self.r.rank16
            elif str_move[1] == '5':
                irank = self.r.rank15
            elif str_move[1] == '6':
                irank = self.r.rank14
            elif str_move[1] == '7':
                irank = self.r.rank13
            elif str_move[1] == '8':
                irank = self.r.rank12
            elif str_move[1] == '9':
                irank = self.r.rank11
        elif l == 3:
            if str_move[2] == '0':
                irank = self.r.rank10
            elif str_move[2] == '1':
                irank = self.r.rank9
            elif str_move[2] == '2':
                irank = self.r.rank8
            elif str_move[2] == '3':
                irank = self.r.rank7
            elif str_move[2] == '4':
                irank = self.r.rank6
            elif str_move[2] == '5':
                irank = self.r.rank5
            elif str_move[2] == '6':
                irank = self.r.rank4
            elif str_move[2] == '7':
                irank = self.r.rank3
            elif str_move[2] == '8':
                irank = self.r.rank2
            elif str_move[2] == '9':
                irank = self.r.rank1

        move = irank * bo.nrank + ifile
        ma.makemove(bo, move, self.color, self.ply, self.f, self.r, bi, self.st)
        self.rec.moves.append(best_sq)
        self.ply += 1
        self.set_kou(bo, bi, move)