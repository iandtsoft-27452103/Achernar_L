import torch
import torch.nn as nn
import torchvision
import torch.functional as F
import policy
import policy_conv3d
import policy_lazy
import value
import file
import rank
import bitop
import stone
import makemove
import feature
import board
import think
import numpy
class test:
    def test1(self, rec, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)

        color = 0
        for ply in range(1, len(rec.moves) + 1):
            current = rec.moves[ply - 1]

            if ply == 96:
                x = 0
                #x = ft.make_input_features(bo, color, rec, ply - 2)

            ma.makemove(bo, current, color, ply, f, r, bi, st)
            if ply == 228:
                self.out_board(bo, current)

            color = color ^ 1
    
    def test3(self, records, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)
        th = think.think()

        device = torch.device("cuda:0")
        model = policy.policy()
        model.load_state_dict(torch.load('model.pth'))
        model = model.to(device)

        total_move_count = 0
        total_match_count = 0

        for cnt in range(40):

            color = 0
            move_count = 0
            match_count = 0
            bo = board.board()
            for ply in range(1, len(records[cnt].moves) + 1):
                current = records[cnt].moves[ply - 1]
                li = []
                fe = ft.make_input_features(bo, records[cnt], ply - 2)
                li.append(fe)
                li = numpy.array(li)

                model.eval()

                with torch.no_grad():
                    x = torch.tensor(li, dtype = torch.float)
                    x = x.to(device)
                    y = model.forward(x)
                    y = y.to("cpu")

                    bb_full = (1 << 361) - 1
                    #cnt = bi.popu_count(bb_full)
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
                    for i in range(len(moves)):
                        b = z[1][moves[i]]
                        digits.append(b)
                        if b > correct_digit:
                            flag = True

                    ma.makemove(bo, current, color, ply, f, r, bi, st)
                    if flag == False:
                        match_count += 1
                color = color ^ 1
                move_count += 1

            matching_rate = match_count / move_count
            print("[record ", cnt + 1, "]")
            print(match_count, "/", move_count, " ", matching_rate)
            print("")

            total_match_count += match_count
            total_move_count += move_count
        
        total_matching_rate = total_match_count / total_move_count
        print("[total]")
        print(total_match_count, "/", total_move_count, total_matching_rate)

    #Value Network検定用
    #※unmakemoveを使っていないので遅い
    def test4(self, records, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)
        th = think.think()

        device = torch.device("cuda:0")
        model = value.value()
        model.load_state_dict(torch.load('model_value.pth'))
        model = model.to(device)

        #total_move_count = 0
        #total_match_count = 0

        cnt = 352

        #color = 0
        move_count = 0
        match_count = 0
        print("moves = ", len(records[cnt].moves))
        #bo = board.board()
        for ply in range(1, len(records[cnt].moves) + 1):
            print("ply = ", ply)

            teacher_move = records[cnt].moves[ply - 1]
            bb_full = (1 << 361) - 1
            bb_move = bi.bb_not_and(bb_full, bo.bb_occupied)

            moves = []
            win_rates = []
            teacher_win_rate = 0
            flag = False
            while bb_move != 0:
                sq = bi.first_one(bb_move)
                bb_move = bi.xor(sq, bb_move)
                #コウでない
                if sq != bo.kou:
                    #合法手である
                    if th.is_move_valid(bo, bi, sq, st) == 0:
                        moves.append(sq)
            
            li = []
            batch_size = 128
            for i in range(len(moves)):
                color = 0
                bo = board.board()
                for j in range(len(records[cnt].moves)):
                    current = records[cnt].moves[j]
                    ma.makemove(bo, current, color, ply, f, r, bi, st)
                    color = color ^ 1
                move = moves[i]
                ma.makemove(bo, move, color, ply, f, r, bi, st)
                fe = ft.make_input_features(bo, records[cnt], ply - 1)
                li.append(fe)
                with torch.no_grad():
                    li = numpy.array(li)
                    x = torch.tensor(li, dtype = torch.float)
                    x = x.to(device)
                    y = model.forward(x)
                    y = y.to("cpu")
                    z = y.sigmoid()
                    z = z.data[0].tolist()
                    z = 1 - z
                    if move == teacher_move:
                        teacher_win_rate = z
                    win_rates.append(z)
                    li = []

            for i in range(len(win_rates)):
                current_win_rate = win_rates[i]
                if current_win_rate > teacher_win_rate:
                    flag = True
                    break

            if flag == False:
                match_count += 1
                print("match")
            else:
                print("unmatch")

            move_count += 1

        matching_rate = match_count / move_count
        #print("[record ", cnt + 1, "]")
        print(match_count, "/", move_count, " ", matching_rate)
        print("")

    def test5(self, records, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)
        th = think.think()

        device = torch.device("cuda:0")
        model = policy.policy()
        model.load_state_dict(torch.load('model.pth'))
        model = model.to(device)

        total_move_count = 0
        total_match_count = 0

        for cnt in range(len(records)):
        #for cnt in range(40):

            bs_list = []
            batch_size = 64
            batch_cnt = records[cnt].ply // batch_size
            remainder = records[cnt].ply - batch_cnt * batch_size
            for i in range(batch_cnt):
                bs_list.append(batch_size)
            if remainder != 0:
                bs_list.append(remainder)

            color = 0
            move_count = 0
            match_count = 0
            batch_number = 0
            i = 0
            fe_list = []
            result_list = []
            bo = board.board()

            for ply in range(1, len(records[cnt].moves) + 1):
                current = records[cnt].moves[ply - 1]
                fe = ft.make_input_features(bo, records[cnt], ply - 2)
                fe_list.append(fe)

                ma.makemove(bo, current, color, ply, f, r, bi, st)

                color = color ^ 1

                i += 1
                if i == bs_list[batch_number]:
                    x = numpy.array(fe_list)

                    model.eval()
                    with torch.no_grad():
                        x = torch.tensor(x, dtype = torch.float)
                        x = x.to(device)
                        model.batch_size = i
                        y = model.forward(x)
                        y = y.to("cpu")
                        for j in range(bs_list[batch_number]):
                            z = y[j].tolist()
                            result_list.append(z)

                    batch_number += 1
                    i = 0
                    fe_list = []

            color = 0    
            bo = board.board()
            for ply in range(1, len(result_list) + 1):
                current = records[cnt].moves[ply - 1]

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

                z = result_list[ply - 1]

                correct_digit = z[1][current]

                digits = []
                flag = False
                for i in range(len(moves)):
                    b = z[1][moves[i]]
                    digits.append(b)
                    if b > correct_digit:
                        flag = True

                ma.makemove(bo, current, color, ply, f, r, bi, st)
                if flag == False:
                    match_count += 1
                color = color ^ 1
                move_count += 1

            matching_rate = match_count / move_count
            print("[record ", cnt + 1, "]")
            print(match_count, "/", move_count, " ", matching_rate)
            print("")

            total_match_count += match_count
            total_move_count += move_count
        
        total_matching_rate = total_match_count / total_move_count
        print("[total]")
        print(total_match_count, "/", total_move_count, total_matching_rate)

    def test6(self, records, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)
        th = think.think()

        device = torch.device("cuda:0")
        model = policy_conv3d.policy()
        model.load_state_dict(torch.load('model.pth'))
        model = model.to(device)

        total_move_count = 0
        total_match_count = 0

        #for cnt in range(len(records)):
        for cnt in range(40):

            bs_list = []
            batch_size = 64
            batch_cnt = records[cnt].ply // batch_size
            remainder = records[cnt].ply - batch_cnt * batch_size
            for i in range(batch_cnt):
                bs_list.append(batch_size)
            if remainder != 0:
                bs_list.append(remainder)

            color = 0
            move_count = 0
            match_count = 0
            batch_number = 0
            i = 0
            fe_list = []
            result_list = []
            bo = board.board()

            for ply in range(1, len(records[cnt].moves) + 1):
                current = records[cnt].moves[ply - 1]
                fe = ft.make_input_features2(bo, records[cnt], ply - 2, color)
                fe_list.append(fe)

                ma.makemove(bo, current, color, ply, f, r, bi, st)

                color = color ^ 1

                i += 1
                if i == bs_list[batch_number]:
                    x = numpy.array(fe_list)
                    x = x.reshape(i, 2, 19, 19, 19)

                    model.eval()
                    with torch.no_grad():
                        x = torch.tensor(x, dtype = torch.float)
                        x = x.to(device)
                        model.batch_size = i
                        y = model.forward(x)
                        y = y.to("cpu")
                        for j in range(bs_list[batch_number]):
                            z = y[j].tolist()
                            result_list.append(z)

                    batch_number += 1
                    i = 0
                    fe_list = []

            color = 0    
            bo = board.board()
            for ply in range(1, len(result_list) + 1):
                current = records[cnt].moves[ply - 1]

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

                z = result_list[ply - 1]

                correct_digit = z[1][current]

                digits = []
                flag = False
                for i in range(len(moves)):
                    b = z[1][moves[i]]
                    digits.append(b)
                    if b > correct_digit:
                        flag = True

                ma.makemove(bo, current, color, ply, f, r, bi, st)
                if flag == False:
                    match_count += 1
                color = color ^ 1
                move_count += 1

            matching_rate = match_count / move_count
            print("[record ", cnt + 1, "]")
            print(match_count, "/", move_count, " ", matching_rate)
            print("")

            total_match_count += match_count
            total_move_count += move_count
        
        total_matching_rate = total_match_count / total_move_count
        print("[total]")
        print(total_match_count, "/", total_move_count, total_matching_rate)

    def test7(self, records, bo):
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)
        th = think.think()

        device = torch.device("cuda:0")
        model = policy_lazy.policy()
        model.load_state_dict(torch.load('model_lazy.pth'))
        model = model.to(device)

        total_move_count = 0
        total_match_count = 0

        #for cnt in range(len(records)):
        for cnt in range(40):

            bs_list = []
            batch_size = 64
            batch_cnt = records[cnt].ply // batch_size
            remainder = records[cnt].ply - batch_cnt * batch_size
            for i in range(batch_cnt):
                bs_list.append(batch_size)
            if remainder != 0:
                bs_list.append(remainder)

            color = 0
            move_count = 0
            match_count = 0
            batch_number = 0
            i = 0
            fe_list = []
            result_list = []
            bo = board.board()

            for ply in range(1, len(records[cnt].moves) + 1):
                current = records[cnt].moves[ply - 1]
                fe = ft.make_input_features(bo, records[cnt], ply - 2, color)
                fe_list.append(fe)

                ma.makemove(bo, current, color, ply, f, r, bi, st)

                color = color ^ 1

                i += 1
                if i == bs_list[batch_number]:
                    x = numpy.array(fe_list)

                    model.eval()
                    with torch.no_grad():
                        x = torch.tensor(x, dtype = torch.float)
                        x = x.to(device)
                        model.batch_size = i
                        y = model.forward(x)
                        y = y.to("cpu")
                        for j in range(bs_list[batch_number]):
                            z = y[j].tolist()
                            result_list.append(z)

                    batch_number += 1
                    i = 0
                    fe_list = []

            color = 0    
            bo = board.board()
            for ply in range(1, len(result_list) + 1):
                current = records[cnt].moves[ply - 1]

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

                z = result_list[ply - 1]

                correct_digit = z[1][current]

                digits = []
                flag = False
                for i in range(len(moves)):
                    b = z[1][moves[i]]
                    digits.append(b)
                    if b > correct_digit:
                        flag = True

                ma.makemove(bo, current, color, ply, f, r, bi, st)
                if flag == False:
                    match_count += 1
                color = color ^ 1
                move_count += 1

            matching_rate = match_count / move_count
            print("[record ", cnt + 1, "]")
            print(match_count, "/", move_count, " ", matching_rate)
            print("")

            total_match_count += match_count
            total_move_count += move_count
        
        total_matching_rate = total_match_count / total_move_count
        print("[total]")
        print(total_match_count, "/", total_move_count, total_matching_rate)

    def out_board(self, bo, move):
        for i in range(bo.nrank):
            s = ""
            for j in range(bo.nfile):
                idx = i * 19 + j
                if bo.board[idx] == 0:
                    s += "○"
                elif bo.board[idx] == 1:
                    s += "●"
                else:
                    s += "＋"

                if j == 18:
                    print(s)