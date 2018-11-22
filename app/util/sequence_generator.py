from random import choice


def hammingDistance(s1 = "", s2 = ""):
    """Return the Hamming distance between sequences"""
    # if len(s1) != len(s2):
    #    raise ValueError("Undefined for sequences of unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))


def rand_seq(l=11):
    return "".join(choice("ATCG") for i in range(l))

class qStaple:
    def __init__(self, staple = None):
        if staple:
            self.short = staple.short
            self.long1 = staple.long1
            self.long2 = staple.long2

    def from_seq(self, seq, seq_map=(11,11,10)):
            self.short = seq[0 : sum(seq_map[:1])]
            self.long1 = seq[sum(seq_map[:1]) : sum(seq_map[:2])]
            self.long2 = seq[sum(seq_map[:2]) : sum(seq_map[:3])]

    def __str__(self):
        return "".join([self.short,self.long1,self.long2])

class SequencePool:
    def __init__(self):
        self.pool = []


    def __gc(self, s):
        sm = 0.0
        for c in s:
            if c is "C" or c is "G":
                sm += 1.0
        return sm / len(s)

    def __cond(self, s):
        # s has to be not in the pool
        cond1 = not s in self.pool
        # s has to have a hamming distance of 7 to any oligo in the pool
        gc = self.__gc(s)
        cond2 = gc  > 0.35 and gc <= 0.5
        return cond1 and cond2

    def add_staple(self, staple):
        seq = "".join([staple.short, staple.long1, staple.long2])
        self.pool.append(seq)

    def get_next(self, l=32):
        while True:
            s = rand_seq(l)
            if self.__cond(s):
                self.pool.append(s)
                break
        qst = qStaple()
        qst.from_seq(s)
        return qst





#sp = SequencePool()
#seq = sp.get_next()
#print(seq)