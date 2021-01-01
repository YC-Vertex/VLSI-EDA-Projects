from prj2_graph import *

def search(DFG, IG, pstart, pn, dt):
	if pn.op in ['i', 'o']:
		return
	# delay unit found
	if pn.op == 'd':
		for pe in pn.oEdges:
			search(DFG, IG, pstart, pe.nodes[1], dt - DFG.T0)
	# function unit (+/*) found
	else:
		IG.addEdge(pstart.index, pn.index, dt)

def GenerateIG(DFG):
	IG = InequalityGraph()
	for pn in DFG.AllNodes.values():
		if pn.op in ['i', 'o', 'd']:
			continue
		for pe in pn.oEdges:
			search(DFG, IG, pn, pe.nodes[1], DFG.getDelay(pn.op))
	return IG

def ASAP(IG, S):
	while len(S) > 0:
		Snew = list()
		for pn in S:
			for pe in pn.oEdges:
				flag = pe.nodes[1].updateMob(minT = pn.mob[0] + pe.delay)
				if flag:
					Snew.append(pe.nodes[1])
		S = Snew

def ALAP(IG, S):
	while len(S) > 0:
		Snew = list()
		for pn in S:
			for pe in pn.iEdges:
				flag = pe.nodes[0].updateMob(maxT = pn.mob[1] - pe.delay)
				if flag:
					Snew.append(pe.nodes[0])
		S = Snew
