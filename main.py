from read import Read
import h5py
import glob
import os

fast5_directory = 'data'
fastq_directory = 'data'

data:dict[str, Read] = {}

# read data from fastq files

for fq in glob.glob(fastq_directory+'/*.fastq'):
    with open(fq, 'r') as F:
        while F:
            header = F.readline()[:-1]
            sequence = F.readline()[:-1]
            F.readline()  # +
            quality = F.readline()[:-1]

            if not header:
                F.close()
                break
            
            new_read:Read = Read()
            new_read.load_from_fastq(header, sequence, quality)
            
            data[new_read.id] = new_read


# read data froom fast5 files, computes move and output in fast5 format

for f5 in glob.glob(fast5_directory+'/*.fast5'):
    with h5py.File(f5, 'r') as F:
        os.mkdir('out')
        out = h5py.File('out/'+f5.split('/')[-1], 'w')
        for read in F.keys():
            id = read.split('_')[1]
            signal = list(F[read]['Raw']['Signal'])
            data[id].load_from_fast5(id, signal)
            data[id].generate_move()
            F.copy(read, out)
            out.create_dataset(read+'/Move', data=data[id].move, compression='gzip')
    