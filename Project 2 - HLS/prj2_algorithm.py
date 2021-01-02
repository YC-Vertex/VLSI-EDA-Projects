import random
import copy

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
	IG = InequalityGraph(DFG.T0)
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

def GenerateFirstSolution(IG):
	while True:
		mobList = sorted(IG.AllNodes.items(), key = lambda kv : (kv[1].mob[1] - kv[1].mob[0], kv[0]))
		for i in range(len(mobList)):
			mobList[i] = (mobList[i][0], mobList[i][1].mob[1] - mobList[i][1].mob[0])

		if mobList[0][1] < 0:
			return False
		for item in mobList:
			if item[1] > 0:
				break
		else:
			return True

		index = item[0]
		pn = IG.AllNodes[index]
		if pn.mob[0] == -float('inf') and pn.mob[1] == float('inf'):
			t = 0
		elif pn.mob[0] == -float('inf'):
			t = pn.mob[1]
		elif pn.mob[1] == float('inf'):
			t = pn.mob[0]
		else:
			t = random.randint(pn.mob[0], pn.mob[1])
		pn.mob = [t, t]

		ASAP(IG, [pn])
		ALAP(IG, [pn])

def GetCost(IG, DFG):
	T0 = DFG.T0
	sumCount = [0] * T0
	multCount = [0] * T0
	for pn in IG.AllNodes.values():
		t = pn.mob[0]
		if DFG.AllNodes[pn.index].op == '+':
			sumCount[t % T0] += 1
		else:
			multCount[t % T0] += 1
			multCount[(t+1) % T0] += 1
	return max(sumCount) + 2 * max(multCount)

def GetSchedule(IG):
	schedule = dict()
	for pn in IG.AllNodes.values():
		schedule[pn.index] = pn.mob[0]
	return schedule

def SearchNeighborhood(IG, DFG, tabuList):
	T0 = DFG.T0
	bestSol = None
	minCost = float('inf')

	for pn in IG.AllNodes.values():
		# IG深拷贝
		tempIG = copy.deepcopy(IG)
		# 选择重新调度的结点
		target = tempIG.AllNodes[pn.index]
		target.mob = [-float('inf'), float('inf')]
		# 重新调度
		S = list(tempIG.AllNodes.values())
		S.remove(target)
		ASAP(tempIG, S)
		ALAP(tempIG, S)
		# 对调度进行修正
		if target.mob[0] == -float('inf') and target.mob[1] == float('inf'):
			target.mob = [0, T0 - 1]
		elif target.mob[0] == -float('inf'):
			target.mob[0] = target.mob[1] - T0 + 1
		elif target.mob[1] == float('inf'):
			target.mob[1] = target.mob[0] + T0 - 1
		# 找到改变pn结点时，邻域中的最优解
		bestT = None
		mobBackup = target.mob[:]
		for t in range(target.mob[0], target.mob[1] + 1):
			target.mob = [t, t]
			# 避开被标记为tabu的解
			if GetSchedule(tempIG) in tabuList:
				continue
			# 计算cost
			cost = GetCost(tempIG, DFG)
			if cost < minCost:
				minCost = cost
				bestT = t
			target.mob = mobBackup[:]
		# 如果产生了新的最优解
		if bestT != None:
			target.mob = [bestT, bestT]
			bestSol = tempIG

	return bestSol, minCost

def TabuSearch(IG, DFG, iters, tabuSize):
	T0 = DFG.T0

	# 记录最好的调度
	minCost = float('inf')
	bestSol = None
	# 记录曾经访问过的调度
	tabuList = list()

	# 搜索
	for i in range(iters):
		bestN, costN = SearchNeighborhood(IG, DFG, tabuList)
		# 如果邻域内没有可移动的点，则退出
		if bestN == None:
			break
		# 如果邻域内最优解同时也是全局优解，则更新
		if costN < minCost:
			minCost = costN
			bestSol = bestN
		# 将访问记录至tabu列表
		tabuList.append(GetSchedule(bestN))
		if len(tabuList) > tabuSize:
			tabuList.pop(0)

	return bestSol

def Assignment(sol, DFG):
	T0 = DFG.T0
	return