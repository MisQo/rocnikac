from read import Read
import h5py
import glob
import os
import numpy as np

def read_fast5_file(file):
    reads = []
    with h5py.File(file, 'r') as F:
        for read in F.keys():
            id = read
            signal = np.array(F[read]['Raw']['Signal'])
            fastq = F[read]['Analyses']['Basecall_1D_000']['BaseCalled_template']['Fastq'][()].decode().split('\n')
            start = int(F[read]['Analyses/Segmentation_000/Summary/segmentation'].attrs['first_sample_template'])
            r = Read(id, start)
            r.load_from_fast5(id, signal[start:])
            r.load_from_fastq(fastq[0], fastq[1], fastq[3])
            reads.append(r)
    return reads

def read_fast5_multiple(directory):
    res = {}
    for f5 in glob.glob(directory + '/*.fast5'):
        res[f5] = read_fast5_file(f5)
    return res

def output_move(original_file, reads):
    try:
        os.mkdir('out')
    except:
        pass
    file = h5py.File(original_file, 'r')
    out = h5py.File('out/'+original_file.split('/')[-1], 'w')
    for r in reads:
        file.copy(r.id, out)
        out.create_dataset(r.id+'/Analyses/Move', data=[0 for _ in range(r.start)] + r.move, compression='gzip')
