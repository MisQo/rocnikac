from fast5 import *
from heuristic import Heuristic
from lazy import Lazy
from naive import Naive

read = read_fast5_file('data/train/SP1-mapped0.fast5')

algs = [Lazy(3), Naive(3)]
for x in [1, 2, 3, 5, 7, 10, 15, 20, 30]:
    for w in [10, 20, 50, 100, 200, 400, 600, 1000, 2000, 10000]:
        algs.append(Heuristic(2, 10, 3, x, w))

print([str(a) for a in algs])
input()

for a in algs:
    t, s, e = a.test_multiple(read)
    with open('out/test/'+str(a), 'w') as f:
        print(t, s, e, file=f)
