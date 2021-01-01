import sys

from prj2_graph import *
from prj2_input import *
from prj2_algorithm import *

def Project2(argc, argv):
	# input, construct DFG
	DFG = DataFlowGraph()
	if argc >= 2:
		infile = open(argv[1], 'r')
		DFG = InputFile(infile)
	else:
		DFG = InputConsole()

	# transform DFG into inequality graph
	IG = GenerateIG(DFG)
	# debug output
	IG.showEdges()

	# nRef = list(IG.AllNodes.values())[0]
	nRef = IG.AllNodes['2']
	nRef.updateMob(0, 0)
	# use Bellman-Ford alg to compute ASAP scheduling
	S = [nRef]
	ASAP(IG, S)
	# use Bellman-Ford alg to compute ALAP scheduling
	S = [nRef]
	ALAP(IG, S)
	# debug output
	IG.showNodes()


if __name__ == '__main__':
	Project2(len(sys.argv), sys.argv)
