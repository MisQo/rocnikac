import h5py
import glob
import numpy as np

fast5_directory = 'data'

table = {}

for l in open('template_median68pA.model'):
    x = l.split()
    table[x[0]] = float(x[1])


mean = np.mean(list(table.values()))
std = np.std(list(table.values()))

with open('table', 'w') as f:
    for kmer, signal in table.items():
        print(kmer, (signal-mean)/std, file=f)
        table[kmer] = (signal-mean)/std

with open('table.cpp', 'w') as f:
    print('#include <vector>', file=f)
    print('std::vector<double> table = {', file=f)
    t = list(table.values())
    for i in range(len(t)):
        print(str(t[i]) + ('};' if i+1 == len(table.values()) else ','), file=f)

with open('table.py', 'w') as f:
    print('table = ' + str(table), file=f)
