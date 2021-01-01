import sys

from prj2_graph import *
from prj2_input import *
from prj2_algorithm import *

def Project2(argc, argv):
	DFG = DataFlowGraph()
	if argc >= 2:
		infile = open(argv[1], 'r')
		DFG = InputFile(infile)
	else:
		DFG = InputConsole()

	IG = GenerateIG(DFG)
	IG.showEdges()

if __name__ == '__main__':
	Project2(len(sys.argv), sys.argv)
