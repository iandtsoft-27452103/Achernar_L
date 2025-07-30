from xmlrpc.client import MAXINT, MININT
import torch
import torch.nn as nn
import torch.functional as F
import numpy
import policy_lazy
import value_lazy
import board
import inout
#import result
import file
import rank
import bitop
import stone
#import makemove
import feature
import color as C
import valid

def main():

    #bo = board.board()
    #cls_io = inout.inout()
    #cls_io.read_records('20220403_nhk_hai.txt')
    #t = test3.test3()
    #t.test4(cls_io.rec, bo)
    #a = analyze.analyze()
    #a.analyze_policy(cls_io.rec[0], bo)
    #return
    try:
        device = torch.device("cuda:0")
        model = policy_lazy.policy()
        model.load_state_dict(torch.load('model_lazy.pth'))
        model = model.to(device)
        model_value = value_lazy.value()
        model_value.load_state_dict(torch.load('model_value_lazy.pth'))
        model_value = model_value.to(device)
        bo = board.board()
        ft = feature.feature(bo)
        bi = bitop.bitop(bo)
        st = stone.stone()
        c = C.color()
        va = valid.valid()
        cm = ','
        move_limit = 8
        print('Hello World.')

        cmd_line = ''
        #str_test_p = 'p,0011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102-0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-None,1011201021121002102001120102102100010200112010210210021220011201021021002102002120102102100210200112010210210021020011201021021002102001120102102000210200112010210210021020011202021021002102001120102102100210210112010210210021020011200021021002102001120102102100210200111010210210021020001201021021002102001220102102100210200112010210210020020011201021021002102-50-51-52-53-54-55-56-57-58-59-60-61-62-63-64-65-66-67-68-69-70-71-72-73-74-75-76-77-78-79-80-81-82-83-84-85-86-87-88-89-333'
        str_test_p = 'p,0011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102-0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-None-b'
        #str_test_v = 'v,0011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102001120102102100210200112010210210021020011201021021002102-0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-None-b,1011201021121002102001120102102100010200112010210210021220011201021021002102002120102102100210200112010210210021020011201021021002102001120102102000210200112010210210021020011202021021002102001120102102100210210112010210210021020011200021021002102001120102102100210200111010210210021020001201021021002102001220102102100210200112010210210020020011201021021002102-50-51-52-53-54-55-56-57-58-59-60-61-62-63-64-65-66-67-68-69-70-71-72-73-74-75-76-77-78-79-80-81-82-83-84-85-86-87-88-89-333-w'
        #cmd_line = str_test_v
        model.eval()
        model_value.eval()

        #1度実行しておくと初回の計算が速くなる。理由は不明。
        with torch.no_grad():
            temp = torch.zeros((1,44,19,19), dtype=torch.float, device=device)
            _ = model.forward(temp)
            model_value.batch_size = 1
            temp = torch.zeros((1,44,19,19), dtype=torch.float, device=device)
            _ = model_value.forward(temp)

        while True:
            cmd_line = input()
            #cmd_line = str_test_p
            cmd = cmd_line.split(',')
            batch_size = len(cmd) - 1
            if cmd[0] == 'quit':
                break
            str_mode = cmd[0]
            features = []
            for i in range(1, len(cmd)):
                input_feature = []
                #print(i)
                cmd2 = cmd[i].split('-')
                #print(cmd2)
                fe_black_stone = numpy.zeros(shape=(361))
                fe_white_stone = numpy.zeros(shape=(361))
                fe_empty = numpy.zeros(shape=(361))
                bb_empty = bi.bb_ini()
                for j in range(361):
                    if cmd2[0][j] == '0':
                        fe_black_stone[j] = 1
                    elif cmd2[0][j] == '1':
                        fe_white_stone[j] = 1
                    else:
                        fe_empty[j] = 1
                        bb_empty = bi.xor(j, bb_empty)
                input_feature.append(fe_black_stone)
                input_feature.append(fe_white_stone)
                input_feature.append(fe_empty)
                fe_prev_move = numpy.zeros(shape=(40,361))
                for j in range(40):
                    if cmd2[j + 1] != str(bo.square_nb):
                        fe_prev_move[j][int(cmd2[j + 1])] = 1
                    input_feature.append(fe_prev_move[j])
                a = cmd2[len(cmd2) - 1]
                if a == 'b':
                    f = numpy.zeros(shape=(361))
                    va.color = c.black
                else:
                    f = numpy.ones(shape=(361))
                    va.color = c.white
                input_feature.append(f)
                if cmd2[len(cmd2) - 1] == 'None':
                    bo.kou = bo.square_nb
                else:
                    bo.kou = cmd2[len(cmd2) - 1]
                features.append(input_feature)
            #print(features)
            features = numpy.array(features)
            x = torch.tensor(features, dtype=torch.float, device=device)
            str_ret = ''
            if str_mode == 'p':
                with torch.no_grad():
                    x = x.reshape(batch_size, 44, 19, 19)
                    model.batch_size = batch_size
                    y = model.forward(x)
                    y = y.reshape(batch_size, 2, 361)
                    #param = y.tolist()
                    
                    for i in range(batch_size):
                        param = y[i][1].tolist()
                        #bb_full = (1 << 361) - 1
                        #cnt = bi.popu_count(bb_full)
                        #bb_move = bi.bb_and(bb_full, bb_empty)

                        #move = []
                        #while bb_move != 0:
                            #sq = bi.first_one(bb_move)
                            #bb_move = bi.xor(sq, bb_move)
                            #move.append(sq)
                            #exclamation: MakeMoveしていないので合法手チェックはできない
                            # C#側でチェックする
                            #コウでない
                            #if sq != bo.kou:
                                #合法手である
                                #if va.is_move_valid(bo, bi, sq, st) == 0:
                                    #move.append(sq)
                            
                        #ToDoリスト
                        #(1) 着手可能箇所が12未満になった場合のPolicy Networkの処置→全部候補手にする
                        #(2) Value Networkの動作確認
                        #(3) 可能であればPolicy Networの結果をSoftmax関数を通してC#に返す
                        #if len(move) < move_limit:
                            #move_limit = len(move)

                        #li_score = []
                        #for j in range(len(move)):
                            #li_score.append(param[j])
                            
                        #li_score = numpy.array(li_score)
                        param = numpy.array(param)
                        li_m = []
                        li_s = []
                        for j in range(move_limit):
                            idx = numpy.argmax(param)
                            li_m.append(idx)
                            #li_m.append(idx)
                            li_s.append(param[idx])
                            param[idx] = MININT
                            
                        li_s = torch.tensor(li_s, dtype=torch.float)
                        li_s = torch.softmax(li_s, dim=0)
                        li_s = li_s.tolist()

                        for j in range(len(li_m)):
                            if j != 0:
                                str_ret += cm
                            str_ret += str(li_m[j]) + ' ' + str(li_s[j])
                        if i != batch_size - 1:
                            str_ret += ':'
                            
            elif str_mode == 'v':
                with torch.no_grad():
                    x = x.reshape(batch_size, 44, 19, 19)
                    model.batch_size = batch_size
                    y = model_value.forward(x)
                    y = torch.sigmoid(y)
                    y = y.tolist()
                    for i in range(batch_size):
                        if i != 0:
                            str_ret += cm
                        str_ret += str(y[i])
            if str_ret != '':
                print(str_ret)
            #break

        #for i in range(1000000000):
            #x = 0
    except Exception:
        fi = open('error_log.txt', 'w', 1, 'UTF-8')
        fi.write(cmd_line)
        fi.close()

if __name__ == "__main__":
    main()