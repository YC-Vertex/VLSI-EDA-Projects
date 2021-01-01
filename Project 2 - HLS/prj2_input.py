from prj2_graph import *

def InputFile(infile):
	nCount = int(infile.readline())
	eCount = int(infile.readline())
	T0 = int(infile.readline())
	DFG = DataFlowGraph(T0)
	for i in range(nCount):
		s = infile.readline().split()
		index = s[0]
		op = s[1]
		DFG.addNode(index, op)
	for i in range(eCount):
		s = infile.readline().split()
		n1 = s[0]
		n2 = s[1]
		DFG.addEdge(n1, n2)
	return DFG

def InputConsole():
	nCount = int(input())
	eCount = int(input())
	T0 = int(input())
	DFG = DataFlowGraph(T0)
	for i in range(nCount):
		s = input().split()
		index = s[0]
		op = s[1]
		DFG.addNode(index, op)
	for i in range(eCount):
		s = input().split()
		n1 = s[0]
		n2 = s[1]
		DFG.addEdge(n1, n2)
	return DFG	
