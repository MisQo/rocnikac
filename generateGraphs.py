import numpy as np
import matplotlib.pyplot as plt
from table import table
from fast5 import *
from heuristic import Heuristic


def plot_signal_match(read, alg):
    alg.generate_move(read)
    predicted = []
    p = 0
    for i in range(len(read.signal)):
        if read.move[i] == 1:
            p += 1
            l = i
        predicted.append(table[read.sequence[p:p+6]])
    plt.plot(read.signal, 'k', color='red')
    plt.plot(predicted, 'k', color='blue')
    plt.show()


def plot_tests():
    ranges = [1, 2, 3, 5, 7, 10, 15, 20, 30]
    widths = (10, 20, 50, 100, 200, 400, 600, 1000, 2000, 10000)

    fig, axs = plt.subplots(len(ranges))


    for i, rang in enumerate(ranges):
        time = []
        std = []
        err = []
        for w in widths:
            with open('out/test/'+str(Heuristic(2, 10, 3, rang, w)), 'r') as f:
                t, s, e = f.readline().split()
                time.append(float(t))
                std.append(float(s))
                err.append(float(e))

        values = {
            'time': tuple(time),
            'err': err,
        }



        x = np.arange(len(widths))  # the label locations
        width = 0.25  # the width of the bars
        multiplier = 0


        for attribute, measurement in values.items():
            offset = width * multiplier
            rects = axs[i].bar(x + offset, measurement, width, label=attribute)
            axs[i].bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        axs[i].set_title('range' + str(rang))
        axs[i].set_xlabel('width')
        axs[i].set_xticks(x + width, widths)
        axs[i].legend(loc='upper left', ncols=3)
        axs[i].set_ylim(0, 2)

    plt.show()


if __name__ == "__main__":
    read = read_fast5_file('data/train/SP1-mapped0.fast5')[0]

    alg = [ Heuristic(1, 24, 3, 3, 300),
        Heuristic(1, 24, 3, 7, 800),
        Heuristic(1, 24, 3, 20, 1000)]

    plot_signal_match(read, alg[0])

    # plot_tests()