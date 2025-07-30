import random
import stone

class board:
    def __init__(self):
        self.bb_color = [0, 0]
        self.bb_occupied = 0
        self.square_nb = 361
        s = stone.stone()
        self.board = [s.blank] * self.square_nb
        self.seq_num = [0, 0]
        self.seq_max = 256
        self.seq_number_table = [[self.seq_max for j in range(self.square_nb)] for i in range(2)]
        self.ply_max = 128
        self.bb_seq = [[0 for j in range(self.seq_max)] for i in range(2)]
        self.bb_dame = [[0 for j in range(self.seq_max)] for i in range(2)]
        self.agehama = [0, 0]
        self.saved_agehama = [[0 for j in range(self.ply_max)] for i in range(2)]
        self.hash_key = 0
        self.saved_hash_key = [0] * self.ply_max
        self.connect_flag = [0] * self.ply_max
        self.tori_flag = [0] * self.ply_max
        self.saved_seq_num = [[self.seq_max for j in range(3)] for i in range(self.ply_max)]
        self.saved_seq_bb = [[0 for j in range(3)] for i in range(self.ply_max)]
        self.saved_dame_bb = [[0 for j in range(3)] for i in range(self.ply_max)]
        self.saved_base_seq_num = [self.seq_max] * self.ply_max
        self.saved_base_seq_bb = [0] * self.ply_max
        self.saved_base_dame_bb = [0] * self.ply_max
        self.saved_opp_seq_num = [[self.seq_max for j in range(4)] for i in range(self.ply_max)]
        self.saved_opp_dame_bb = [[0 for j in range(4)] for i in range(self.ply_max)]
        self.saved_made_dame_square = [[self.square_nb for j in range(128)] for i in range(self.ply_max)]
        self.removed_seq_num = [[self.seq_max for j in range(4)] for i in range(self.ply_max)]
        self.removed_seq_bb = [[0 for j in range(4)] for i in range(self.ply_max)]
        self.kou = self.square_nb
        self.kou_array = [self.square_nb] * self.ply_max#探索用
        self.nfile = 19
        self.nrank = 19
        self.file_table = []
        self.init_file_table()
        self.rank_table = []
        self.init_rank_table()
        self.hash = [[0 for j in range(self.square_nb)] for i in range(2)]
        #※ハッシュテーブル初期化処理は外側で呼ぶ

    def init_file_table(self):
        for r in range(self.nrank):
            for f in range(self.nfile):
                self.file_table.append(f)

    def init_rank_table(self):
        for r in range(self.nrank):
            for f in range(self.nfile):
                self.rank_table.append(r)

    #ハッシュテーブル初期化処理
    #initでは呼ばない
    def init_hash_table(self):
        for i in range(2):
            for j in range(self.square_nb):
                self.hash[i][j] = random.randint((1 << 63) + 1, (1 << 64) - 1)