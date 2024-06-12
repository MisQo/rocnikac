from read import Read
import sys
from dynamicRecursive import DynamicRecursive
from dynamicItterative import DynamicItterative
from heuristic import Heuristic
import numpy as np
from sys import stderr
from fast5 import *

fast5_directory = sys.argv[1]

reads = read_fast5_multiple(fast5_directory)

alg = [ Heuristic(1, 24, 3, 3, 300),
        Heuristic(1, 24, 3, 7, 800),
        Heuristic(1, 24, 3, 20, 1000)]

a = alg[2]
for r in reads.values():
    print(a.test_multiple(r))

for f in reads.keys():
    output_move(f, reads[f])
