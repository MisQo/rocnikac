from generateMove import GenerateMove
from table import table
import numpy as np

class DynamicRecursive(GenerateMove):
    def __init__(self, l, r, threads):
        super().__init__(threads)
        self.l = l
        self.r = r

    # Calculates optimal solution given events must by at least l and atmost r apart

    def generate_move(self, read):        
        n = len(read.signal)
        k = len(read.sequence) - 5

        memo = {
           (n, k) : (0, -1)
        }

        def solve(i, t):
            if i + (k - t) * self.l > n or i + (k-t) * self.r < n:
                return (123465789, -1)
            if (i, t) not in memo:
                memo[(i, t)] = (123456789, -1)
                kmer = read.sequence[t:t+6]
                cur = 0
                for x in range(self.l):
                    cur += (read.signal[i+x] - table[kmer]) ** 2
                for x in range(self.l, self.r):
                    memo[(i, t)] = min(memo[(i, t)], (cur + solve(i+x, t+1)[0], i+x))
                    if i+x >= len(read.signal): break
                    cur += (read.signal[i+x] - table[kmer]) ** 2
            return memo[(i, t)]
        

        solve(0, 0)

        read.move = [0 for _ in range(len(read.signal))]
        c = 0
        try:
            for i in range(k-1):
                read.move[memo[(c, i)][1]] = 1
                c = memo[(c, i)][1]
        except:
            print('fail ', end='')
        return read.move
    
    def __str__(self):
        return f"dynamicRecursive l={self.l}, r={self.r}"
        
