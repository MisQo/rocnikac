from generateMove import GenerateMove
class Lazy(GenerateMove):
    def __init__(self, threads):
        super().__init__(threads)

    # distributes evenly
    def generate_move(self, read):   
        read.move = [0 for i in range(len(read.signal))]
        for i in range(1, len(read.sequence)-5):
            read.move[i] = 1
        return read.move
    
    def __str__(self):
        return 'lazy'