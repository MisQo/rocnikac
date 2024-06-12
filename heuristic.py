from generateMove import GenerateMove
from table import table
import heuristicGenerateMove

class Heuristic(GenerateMove):
    def __init__(self, l, r, threads, range, width = 10000):
        super().__init__(threads)
        self.l = l
        self.r = r
        self.width = width
        self.range = range

    # similiar to dynamic approach but only considers localy best width results

    def generate_move(self, read):

        a = (len(read.signal)//(len(read.sequence)-5))
        self.l, self.r = max(1, a-self.range), a+2+2*self.range
        read.move = heuristicGenerateMove.generate_move(
            signal= read.signal,
            sequence= read.sequence,
            l = self.l,
            r = self.r,
            width = self.width
        )
        return read.move
        n = len(read.signal)
        k = len(read.sequence) - 5

        memo = [dict() for _ in range(k+1)]
        memo[0][0] = (0, 0, 0, -1)

        for t in range(k):
            can = list(memo[t].values())
            can.sort()
            for h, s, i, _ in can[:min(len(can), self.width)]:
                cur = 0
                kmer = read.sequence[t:t+6]
                for x in range(self.l):
                    if i+x >= len(read.signal): break
                    cur += (read.signal[i+x] - table[kmer]) ** 2
                for x in range(self.l, self.r):
                    if i+x > len(read.signal): break
                    if i+x + (k-t-1) * self.l <= n and i+x + (k-t-1) * (self.r-1) >= n:
                        if not i+x in memo[t+1]:
                            memo[t+1][i+x] = (123456789, 123456789, -1, -1)
                        memo[t+1][i+x] = min(memo[t+1][i+x], ((cur + s)/(i+x), cur+s, i+x, i))
                    if i+x >= len(read.signal): break
                    cur += (read.signal[i+x] - table[kmer]) ** 2
        read.move = [0 for _ in range(len(read.signal))]
        c = n
        # print(memo)
        try:
            for i in range(k, 1, -1):
                # print(c, i)
                # print('memo', memo[i][c])
                read.move[memo[i][c][3]] = 1
                c = memo[i][c][3]
        except:
            print('fail ', end='')
            print(memo)
            exit(1)

        print(read.move)
        print(heuristicGenerateMove.generate_move(
            signal= read.signal,
            sequence= read.sequence,
            l = self.l,
            r = self.r,
            width = self.width
        ))

        cppmove = heuristicGenerateMove.generate_move(
            signal= read.signal,
            sequence= read.sequence,
            l = self.l,
            r = self.r,
            width = self.width
        )


        assert(read.move == cppmove)

    def __str__(self):
        return f"heuristic r={self.range}, width={self.width}"
