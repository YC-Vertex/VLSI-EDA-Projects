import sys

from prj4_input import *
from prj4_data import *
from prj4_algorithm import *

def Project4(argc, argv):
    # input
    L = Layout(-1, -1, 0)
    if argc >= 2:
        infile = open(argv[1], 'r')
        L = InputFile(infile)
    else:
        L = InputConsole()
    # debug output
    print('input:')
    L.showCells()
    L.showLayout()
    print()

    # initial random placement
    RandomPlacement(L)
    # debug output
    print('initial:')
    L.showCells()
    L.showLayout()
    print()

    # simulated annealing
    L = SimulatedAnnealing(L, 500, 0.2, len(L.AllCells) * 3)
    # debug output
    print()
    print('final:')
    L.showCells()
    L.showLayout()
    print()

# main
if __name__ == '__main__':
    Project4(len(sys.argv), sys.argv)
