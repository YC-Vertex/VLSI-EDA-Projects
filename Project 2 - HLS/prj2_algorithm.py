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
