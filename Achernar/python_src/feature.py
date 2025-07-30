import numpy as np
import inout
import result
import bitop

class feature:
    def __init__(self, bo):
        self.bi = bitop.bitop(bo)
        self.bb_full = self.bi.bb_ini()
        bb = self.bi.bb_ini()
        for i in range(len(bo.board)):
            bb = self.bi.xor(i, bb)
        self.bb_full = bb

    def make_input_features(self, bo, rec, ply, c):
        features = []
        
        #黒石と白石
        for i in range(len(bo.bb_color)):
            bb = bo.bb_color[i]
            ft = np.zeros(bo.nfile * bo.nrank)
            while bb != 0:
                sq = self.bi.first_one(bb)
                bb = self.bi.xor(sq, bb)
                ft[sq] = 1
            #features.append(ft)
            features.append(ft.reshape((bo.nfile, bo.nrank)))
        
        #空白
        bb = self.bi.bb_not_and(self.bb_full, bo.bb_occupied)
        ft = np.zeros(bo.nfile * bo.nrank)
        while bb != 0:
            sq = self.bi.first_one(bb)
            bb = self.bi.xor(sq, bb)
            ft[sq] = 1
        features.append(ft.reshape((bo.nfile, bo.nrank)))

        #40手前までの手
        j = 0
        for i in range(ply, -1, -1):
            sq = rec.moves[i]
            ft = np.zeros(bo.nfile * bo.nrank)
            ft[sq] = 1
            features.append(ft.reshape((bo.nfile, bo.nrank)))
            j += 1
            if j == 34:
                break

        k = 40 - j

        while k != 0:
            ft = np.zeros(bo.nfile * bo.nrank)
            features.append(ft.reshape((bo.nfile, bo.nrank)))
            k -= 1

        #手番 = 1
        if c == 0:
            ft = np.ones(bo.nfile * bo.nrank)
        else:
            ft = np.zeros(bo.nfile * bo.nrank)
        features.append(ft.reshape((bo.nfile, bo.nrank)))

        return features

    def make_input_features2(self, bo, rec, ply, c):
        features = []
        
        #黒石と白石
        for i in range(len(bo.bb_color)):
            bb = bo.bb_color[i]
            ft = np.zeros(bo.nfile * bo.nrank)
            while bb != 0:
                sq = self.bi.first_one(bb)
                bb = self.bi.xor(sq, bb)
                ft[sq] = 1
            #features.append(ft)
            features.append(ft.reshape((bo.nfile, bo.nrank)))
        
        #空白
        bb = self.bi.bb_not_and(self.bb_full, bo.bb_occupied)
        ft = np.zeros(bo.nfile * bo.nrank)
        while bb != 0:
            sq = self.bi.first_one(bb)
            bb = self.bi.xor(sq, bb)
            ft[sq] = 1
        features.append(ft.reshape((bo.nfile, bo.nrank)))

        #34手前までの手
        j = 0
        for i in range(ply, -1, -1):
            sq = rec.moves[i]
            ft = np.zeros(bo.nfile * bo.nrank)
            ft[sq] = 1
            features.append(ft.reshape((bo.nfile, bo.nrank)))
            j += 1
            if j == 34:
                break

        k = 34 - j

        while k != 0:
            ft = np.zeros(bo.nfile * bo.nrank)
            features.append(ft.reshape((bo.nfile, bo.nrank)))
            k -= 1
            
        #手番 = 1
        if c == 0:
            ft = np.ones(bo.nfile * bo.nrank)
        else:
            ft = np.zeros(bo.nfile * bo.nrank)
        features.append(ft.reshape((bo.nfile, bo.nrank)))

        return features

    def make_output_labels(self, bo, move):
        lbl = np.zeros(bo.nfile * bo.nrank)
        lbl[move] = 1
        label = lbl.reshape((bo.nfile, bo.nrank))
        return label