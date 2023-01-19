class Read:
    def __init__(self):
        self.id = None
        self.fasq_header = None
        self.sequence = None
        self.quality = None
        self.raw_signal = None
        self.move = None

    def load_from_fastq(self, header, sequence, quality):
        self.fasq_header = header
        self.sequence = sequence
        self.quality = quality
        if self.id == None:
            self.id = header.split()[0][1:]

    def load_from_fast5(self, id, signal):
        self.raw_signal = signal
        if self.id == None:
            self.id = id    

    # first naive aproach - bases are ecenly distrubuted

    def generate_move(self):
        self.move = [0 for i in range(len(self.raw_signal)//5)]
        for i in range(1, len(self.sequence)):
            self.move[int(len(self.move)/len(self.sequence)*i)] = 1

        # print(self.move)
        # print(self.id, len(self.move), self.move.count(1), len(self.sequence))




