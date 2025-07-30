import torch
import torch.nn as nn
import torchvision
import torch.functional as F
import policy
import policy_lazy
import value
import file
import rank
import bitop
import stone
import makemove
import unmakemove
import feature
import board
import think
import numpy

class analyze:
    def __init__(self):
        self.date_of_game = '2024/02/04'
        self.name_of_category = '第71回NHK杯準々決勝'
        self.black_player = '芝野虎丸名人'
        self.white_player = '河野臨九段'
        self.engine_name = 'Hope Ver.1.0.2'

    def analyze_policy(self, record, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        um = unmakemove.unmakemove()
        ft = feature.feature(bo)
        th = think.think()

        fp = open('analyze_result_policy.txt', 'w', 1, 'UTF-8')

        self.out_header(fp)

        device = torch.device("cuda:0")
        model = policy_lazy.policy()
        model.load_state_dict(torch.load('model.pth'))
        model = model.to(device)

        color = 0
        move_count = 0
        match_count = 0
        black_move_count = 0
        black_match_count = 0
        white_move_count = 0
        white_match_count = 0
        bo = board.board()
        for ply in range(1, len(record.moves) + 1):
            current = record.moves[ply - 1]
            li = []
            fe = ft.make_input_features(bo, record, ply - 2, color)
            li.append(fe)

            li = numpy.array(li)

            model.eval()

            with torch.no_grad():
                x = torch.tensor(li, dtype = torch.float)
                x = x.to(device)
                y = model.forward(x)
                y = y.to("cpu")

                bb_full = (1 << 361) - 1
                bb_move = bi.bb_not_and(bb_full, bo.bb_occupied)

                moves = []
                while bb_move != 0:
                    sq = bi.first_one(bb_move)
                    bb_move = bi.xor(sq, bb_move)
                    #コウでない
                    if sq != bo.kou:
                        #合法手である
                        if th.is_move_valid(bo, bi, sq, st) == 0:
                            moves.append(sq)

                z = y.data[0].tolist()

                correct_digit = z[1][current]

                digits = []
                flag = False
                max_digit = correct_digit#2023/09/25 修正
                for i in range(len(moves)):
                    b = z[1][moves[i]]
                    digits.append(b)
                    if b > max_digit:#2023/09/25 修正
                        max_digit = b#2023/09/25 修正
                        com_move = moves[i]
                        flag = True

                ma.makemove(bo, current, color, ply, f, r, bi, st)
                if flag == False:
                    com_move = current
                    match_count += 1
                    if color == 0:
                        black_match_count += 1
                    else:
                        white_match_count += 1
            if color == 0:
                s = "●"
                black_move_count += 1
            else:
                s = "○"
                white_move_count += 1
            if flag == False:
                s2 = "○"
            else:
                s2 = "×"
            str_record_move = s + str(bo.file_table[current] + 1) + '-' + str(bo.rank_table[current] + 1)
            str_com_move = s + str(bo.file_table[com_move] + 1) + '-' + str(bo.rank_table[com_move] + 1)
            #print(str_record_move)
            fp.write("ply=" + str(ply) + "   pro= " + str_record_move + ",   com= " + str_com_move + ",   result= " + s2 + "\n")
            color = color ^ 1
            move_count += 1

        matching_rate = match_count / move_count
        #print("[record ", cnt + 1, "]")
        #print(match_count, "/", move_count, " ", matching_rate)
        #print("")
        black_matching_rate = black_match_count / black_move_count
        black_matching_rate *= 100
        black_matching_rate = '{a:.2f}'.format(a=black_matching_rate)
        white_matching_rate = white_match_count / white_move_count
        white_matching_rate *= 100
        white_matching_rate = '{a:.2f}'.format(a=white_matching_rate)
        matching_rate = match_count / move_count
        matching_rate *= 100
        matching_rate = '{a:.2f}'.format(a=matching_rate)
        print("")
        fp.write("\n")
        print(match_count, "/", move_count, " ", matching_rate + "%")
        fp.write('黒番一致率：' + str(black_match_count) + " / " + str(black_move_count) + " " + black_matching_rate + "%\n")
        fp.write('\n')
        fp.write('白番一致率：' + str(white_match_count) + " / " + str(white_move_count) + " " + white_matching_rate + "%\n")
        fp.write('\n')
        fp.write('全体一致率：' + str(match_count) + " / " + str(move_count) + " " + matching_rate + "%\n")
        fp.write('\n')
        self.out_footer(fp)
        fp.close()

    def out_header(self, fp):
        fp.write('対局日：' + self.date_of_game + '\n')
        fp.write('\n')
        fp.write('棋戦名：' + self.name_of_category + '\n')
        fp.write('\n')
        fp.write('黒番：' + self.black_player + '\n')
        fp.write('\n')
        fp.write('白番：' + self.white_player + '\n')
        fp.write('\n')

    def out_footer(self, fp):
        fp.write('解析エンジン名：' + self.engine_name)
        fp.write('\n')
