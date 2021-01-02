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
	print('IG generation:')
	IG.showEdges()

    # select reference node
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
	print('ASAP & ALAP scheduling:')
	IG.showNodes()

	# get first solution
	GenerateFirstSolution(IG)
	# debug output
	print('first solution:')
	IG.showNodes()

	# Tabu search
	IG = TabuSearch(IG, DFG, 100, 10)
	schedule = GetSchedule(IG)
	# debug output
	print('optimal solution:')
	IG.showNodes()

	# assignment
	assignment = Assignment(schedule, DFG)


if __name__ == '__main__':
	Project2(len(sys.argv), sys.argv)
