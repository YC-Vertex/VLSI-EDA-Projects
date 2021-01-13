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
	print('----- Inequality Graph -----')
	IG.showEdges()
	print('----------------------------\n')

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
	print('----- ASAP & ALAP scheduling -----')
	IG.showNodes()
	print('----------------------------------\n')

	# get first solution
	GenerateFirstSolution(IG)
	# debug output
	print('----- initial solution -----')
	IG.showNodes()
	print('----------------------------\n')

	# Tabu search
	IG = TabuSearch(IG, DFG, 25, 8)
	# debug output
	print('----- optimal schedule -----')
	IG.showSchedule()
	print('----------------------------\n')

	# assignment
	SumICG, MultICG = Assignment(IG, DFG)
	print('----- assignment -----')
	print(f'\'+\' ops: ({SumICG.colorUsed.index(False) if False in SumICG.colorUsed else len(SumICG.colorUsed)} FUs used)')
	SumICG.showNodes()
	print(f'\'*\' ops: ({MultICG.colorUsed.index(False) if False in MultICG.colorUsed else len(MultICG.colorUsed)} FUs used)')
	MultICG.showNodes()
	print('----------------------\n')


if __name__ == '__main__':
	Project2(len(sys.argv), sys.argv)
