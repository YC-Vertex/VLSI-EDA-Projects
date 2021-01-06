import sys

from prj3_input import *
from prj3_robdd import *

def Project3(argc, argv):
    if argc >= 2:
        infile = open(argv[1], 'r')
        InputFile(infile)
    else:
        InputConsole()


if __name__ == '__main__':
	Project3(len(sys.argv), sys.argv)