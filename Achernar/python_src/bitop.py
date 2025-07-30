#import board
import file
import rank
import direction

class bitop:
    def __init__(self, b):
        self.bb_mask = [0] * b.square_nb
        for i in range(b.square_nb):
            self.bb_mask[i] = 1 << (b.square_nb - i - 1)

        self.aifirst_one = [0] * 524288
        for i in range(524288):
            self.aifirst_one[i] = self.first_one00(b.nrank, i)

        f = file.file()
        r = rank.rank()
        d = direction.direction()
        self.bb_kou_hantei_table = []
        for i in range(b.square_nb):
            bb = self.bb_ini()
            if b.file_table[i] == f.file1 and b.rank_table[i] == r.rank1:
                bb = self.bb_or(bb, self.bb_mask[i + d.east])
                bb = self.bb_or(bb, self.bb_mask[i + d.south])
            elif b.file_table[i] == f.file19 and b.rank_table[i] == r.rank1:
                bb = self.bb_or(bb, self.bb_mask[i + d.west])
                bb = self.bb_or(bb, self.bb_mask[i + d.south])
            elif b.file_table[i] == f.file1 and b.rank_table[i] == r.rank19:
                bb = self.bb_or(bb, self.bb_mask[i + d.north])
                bb = self.bb_or(bb, self.bb_mask[i + d.east])
            elif b.file_table[i] == f.file19 and b.rank_table[i] == r.rank19:
                bb = self.bb_or(bb, self.bb_mask[i + d.north])
                bb = self.bb_or(bb, self.bb_mask[i + d.west])
            elif b.file_table[i] == f.file1 and b.rank_table[i] != r.rank1 and b.rank_table[i] != r.rank19:
                bb = self.bb_or(bb, self.bb_mask[i + d.north])
                bb = self.bb_or(bb, self.bb_mask[i + d.east])
                bb = self.bb_or(bb, self.bb_mask[i + d.south])
            elif b.file_table[i] == f.file19 and b.rank_table[i] != r.rank1 and b.rank_table[i] != r.rank19:
                bb = self.bb_or(bb, self.bb_mask[i + d.north])
                bb = self.bb_or(bb, self.bb_mask[i + d.west])
                bb = self.bb_or(bb, self.bb_mask[i + d.south])
            elif b.file_table[i] != f.file1 and b.file_table[i] != f.file19 and b.rank_table[i] == r.rank1:
                bb = self.bb_or(bb, self.bb_mask[i + d.west])
                bb = self.bb_or(bb, self.bb_mask[i + d.east])
                bb = self.bb_or(bb, self.bb_mask[i + d.south])
            elif b.file_table[i] != f.file1 and b.file_table[i] != f.file19 and b.rank_table[i] == r.rank19:
                bb = self.bb_or(bb, self.bb_mask[i + d.north])
                bb = self.bb_or(bb, self.bb_mask[i + d.west])
                bb = self.bb_or(bb, self.bb_mask[i + d.east])
            else:
                bb = self.bb_or(bb, self.bb_mask[i + d.north])
                bb = self.bb_or(bb, self.bb_mask[i + d.west])
                bb = self.bb_or(bb, self.bb_mask[i + d.east])
                bb = self.bb_or(bb, self.bb_mask[i + d.south])

            self.bb_kou_hantei_table.append(bb)

    def bb_or(self, a, b):
        return (a | b)

    def bb_and(self, a, b):
        return (a & b)

    def bb_not_and(self, a, b):
        return (a & ~b)

    def bb_ini(self):
        return 0

    def bb_not(self, a):
        return (~a)

    def popu_count(self, bb):
        i = 0
        while (bb):
            i += 1
            bb &= bb - 1

        return i

    def xor(self, sq, bb):
        bb ^= self.bb_mask[sq]
        return bb

    def first_one00(self, nrank, stones):
        for i in range(nrank):
            if stones & (1 << (nrank - i - 1)):
                break

        return i

    def first_one(self, bb):
        if bb & ((0x7ffff) << 342):
            return self.aifirst_one[bb >> 342]
        if bb & ((0x7ffff) << 323):
            return self.aifirst_one[bb >> 323] + 19
        if bb & ((0x7ffff) << 304):
            return self.aifirst_one[bb >> 304] + 38
        if bb & ((0x7ffff) << 285):
            return self.aifirst_one[bb >> 285] + 57
        if bb & ((0x7ffff) << 266):
            return self.aifirst_one[bb >> 266] + 76
        if bb & ((0x7ffff) << 247):
            return self.aifirst_one[bb >> 247] + 95
        if bb & ((0x7ffff) << 228):
            return self.aifirst_one[bb >> 228] + 114
        if bb & ((0x7ffff) << 209):
            return self.aifirst_one[bb >> 209] + 133
        if bb & ((0x7ffff) << 190):
            return self.aifirst_one[bb >> 190] + 152
        if bb & ((0x7ffff) << 171):
            return self.aifirst_one[bb >> 171] + 171
        if bb & ((0x7ffff) << 152):
            return self.aifirst_one[bb >> 152] + 190
        if bb & ((0x7ffff) << 133):
            return self.aifirst_one[bb >> 133] + 209
        if bb & ((0x7ffff) << 114):
            return self.aifirst_one[bb >> 114] + 228
        if bb & ((0x7ffff) << 95):
            return self.aifirst_one[bb >> 95] + 247
        if bb & ((0x7ffff) << 76):
            return self.aifirst_one[bb >> 76] + 266
        if bb & ((0x7ffff) << 57):
            return self.aifirst_one[bb >> 57] + 285
        if bb & ((0x7ffff) << 38):
            return self.aifirst_one[bb >> 38] + 304
        if bb & ((0x7ffff) << 19):
            return self.aifirst_one[bb >> 19] + 323
        return self.aifirst_one[bb] + 342
