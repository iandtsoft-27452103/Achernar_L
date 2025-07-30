import record
import result

class inout:
    def __init__(self):
        self.rec = []
    
    #学習用の棋譜を読み込む
    def read_records(self, r):
        file = open('records1.txt', 'r', 1, 'UTF-8')
        i = 0
        for line in file:
            line = line.replace('\n', '')
            s = line.split(',')
            temp = record.record(r)
            temp.black_player = s[0]
            temp.white_player = s[1]
            if s[2][0] == 'B':
                temp.result = r.black_win
            else:
                temp.result = r.white_win
            for j in range(3, len(s)):
                temp.str_moves.append(s[j])
                temp.moves.append(self.str_to_value(s[j]))
            temp.ply = len(temp.moves)
            self.rec.append(temp)
            i += 1
        file.close()

    #テスト用の棋譜を読み込む
    def read_test_records(self, r):
        file = open('test_records.txt', 'r', 1, 'UTF-8')
        i = 0
        for line in file:
            line = line.replace('\n', '')
            s = line.split(',')
            temp = record.record(r)
            temp.black_player = s[0]
            temp.white_player = s[1]
            if s[2][0] == 'B':
                temp.result = r.black_win
            else:
                temp.result = r.white_win
            for j in range(3, len(s)):
                temp.str_moves.append(s[j])
                temp.moves.append(self.str_to_value(s[j]))
            temp.ply = len(temp.moves)
            self.rec.append(temp)
            i += 1
        file.close()

    #解析用の棋譜を読み込む
    def read_analyze_record(self, r):
        file = open('20240204_nhk_hai.txt', 'r', 1, 'UTF-8')
        i = 0
        for line in file:
            line = line.replace('\n', '')
            s = line.split(',')
            temp = record.record(r)
            temp.black_player = s[0]
            temp.white_player = s[1]
            if s[2][0] == 'B':
                temp.result = r.black_win
            else:
                temp.result = r.white_win
            for j in range(3, len(s)):
                temp.str_moves.append(s[j])
                temp.moves.append(self.str_to_value(s[j]))
            temp.ply = len(temp.moves)
            self.rec.append(temp)
            i += 1
        file.close()

    def read_test_records2(self, r):
        file = open('test_records(2).txt', 'r', 1, 'UTF-8')
        i = 0
        for line in file:
            line = line.replace('\n', '')
            s = line.split(',')
            temp = record.record(r)
            temp.black_player = s[0]
            temp.white_player = s[1]
            if s[2][0] == 'B':
                temp.result = r.black_win
            else:
                temp.result = r.white_win
            for j in range(3, len(s)):
                temp.str_moves.append(s[j])
                temp.moves.append(self.str_to_value(s[j]))
            temp.ply = len(temp.moves)
            self.rec.append(temp)
            i += 1
        file.close()

    def str_to_value(self, move):
        file = move[0]
        rank = move[1]
        if file == 'a':
            i = 0
        elif file == 'b':
            i = 1
        elif file == 'c':
            i = 2
        elif file == 'd':
            i = 3
        elif file == 'e':
            i = 4
        elif file == 'f':
            i = 5
        elif file == 'g':
            i = 6
        elif file == 'h':
            i = 7
        elif file == 'i':
            i = 8
        elif file == 'j':
            i = 9
        elif file == 'k':
            i = 10
        elif file == 'l':
            i = 11
        elif file == 'm':
            i = 12
        elif file == 'n':
            i = 13
        elif file == 'o':
            i = 14
        elif file == 'p':
            i = 15
        elif file == 'q':
            i = 16
        elif file == 'r':
            i = 17
        elif file == 's':
            i = 18
        
        if rank == 'a':
            j = 0
        elif rank == 'b':
            j = 19
        elif rank == 'c':
            j = 19 * 2
        elif rank == 'd':
            j = 19 * 3
        elif rank == 'e':
            j = 19 * 4
        elif rank == 'f':
            j = 19 * 5
        elif rank == 'g':
            j = 19 * 6
        elif rank == 'h':
            j = 19 * 7
        elif rank == 'i':
            j = 19 * 8
        elif rank == 'j':
            j = 19 * 9
        elif rank == 'k':
            j = 19 * 10
        elif rank == 'l':
            j = 19 * 11
        elif rank == 'm':
            j = 19 * 12
        elif rank == 'n':
            j = 19 * 13
        elif rank == 'o':
            j = 19 * 14
        elif rank == 'p':
            j = 19 * 15
        elif rank == 'q':
            j = 19 * 16
        elif rank == 'r':
            j = 19 * 17
        elif rank == 's':
            j = 19 * 18

        return (i + j)