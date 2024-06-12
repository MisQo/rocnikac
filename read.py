import numpy as np
class Read:
    def __init__(self, id, start):
        self.id = id
        self.fasq_header = None
        self.sequence = None
        self.quality = None
        self.raw_signal = None
        self.move = None
        self.signal = None
        self.start = start
        self.time = None

    def load_from_fastq(self, header, sequence, quality):
        self.fasq_header = header
        self.sequence = sequence
        self.quality = quality
        if self.id == None:
            self.id = header.split()[0][1:]

    def normalize_signal(self):
        mean = np.mean(self.raw_signal)
        std = np.std(self.raw_signal)
        return [(s-mean)/std for s in self.raw_signal]

    def load_from_fast5(self, id, signal):
        self.raw_signal = signal
        if self.id == None:
            self.id = id
        self.signal = self.normalize_signal()




