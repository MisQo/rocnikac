import time
from table import table
import numpy as np    
from multiprocessing import Pool

def time_decorator(func):
    def f(*args,**kwargs):
        start = time.time()
        ret = func(*args,**kwargs)
        end = time.time()
        print(end-start)
        return end-start, ret
    return f

class GenerateMove:
    def do(self,r):
        return time_decorator(self.generate_move)(r)
    def __init__(self, threads = 1):
        self.threads = threads

    def generate_move(self, read):
        raise NotImplementedError()

    def generate_move_multiple(self, reads):
        if self.threads == 1:
            for r in reads:
                r.time, r.move = self.do(r)
            return

        print(str(self))
        with Pool(3) as pool:
            res = pool.map(self.do, reads)
            for i in range(len(reads)):
                reads[i].time, reads[i].move = res[i]




    def evaluate(self, read):
        err = 0
        p = []
        l = 0
        predicted = []
        for i in range(len(read.signal)):
            if read.move[i] == 1:
                p.append(i-l)
                l = i
            err += (read.signal[i] - table[read.sequence[len(p):len(p)+6]]) ** 2
            predicted.append(table[read.sequence[len(p):len(p)+6]])
        p.append(len(read.signal) - l)
        return min(p), max(p), np.std(p), err, err/len(read.signal)

    def test(self, read):
        time, _ = time_decorator(self.generate_move(read))
        read.time = time
        return (time,) + self.evaluate(read)
        

    def test_multiple(self, reads):
        self.generate_move_multiple(reads)

        time, stdl, avgerr = 0, 0, 0
        for r in reads:
            _, _, st, _, av = self.evaluate(r)
            time += r.time
            stdl += st
            avgerr += av
        n = len(reads)
        return (time)/n, stdl/n, avgerr/n
            

