from generateMove import GenerateMove
from table import table
import numpy as np

class DynamicItterative(GenerateMove):
    def __init__(self, l, r, threads):
        super().__init__(threads)
        self.l = l
        self.r = r

    # Calculates optimal solution given events must by at least l and atmost r apart

    def generate_move(self, read):
        n = len(read.signal)
        k = len(read.sequence) - 5

        memo = [dict() for _ in range(k+1)]
        memo[0][0] = (0, -1)

        for t in range(k):
            for i in memo[t].keys():
                cur = 0
                kmer = read.sequence[t:t+6]
                for x in range(self.l):
                    if i+x >= len(read.signal): break
                    cur += (read.signal[i+x] - table[kmer]) ** 2
                for x in range(self.l, self.r):
                    if i+x > len(read.signal): break
                    if not i+x in memo[t+1]:
                        memo[t+1][i+x] = (123456789, -1)
                    memo[t+1][i+x] = min(memo[t+1][i+x], (cur + memo[t][i][0], i))
                    if i+x >= len(read.signal): break
                    cur += (read.signal[i+x] - table[kmer]) ** 2

        read.move = [0 for _ in range(len(read.signal))]
        c = n
        try:
            for i in range(k, 1, -1):
                read.move[memo[i][c][1]] = 1
                c = memo[i][c][1]
        except:
            print('fail ', end='')
        return read.move

    def __str__(self):
        return f"dynamicitterative l={self.l}, r={self.r}"
