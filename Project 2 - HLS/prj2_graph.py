# node of dataflow graph
class DFGNode:

	def __init__(self, index, operation, delay):
		self.index = index
		self.op = operation
		self.delay = delay
		self.iEdges = list()
		self.oEdges = list()


# edge of dataflow graph
class DFGEdge:

	def __init__(self, pn1, pn2):
		self.nodes = (pn1, pn2)


# dataflow graph
class DataFlowGraph:

	def __init__(self, T0 = -1):
		self.T0 = T0
		self.AllNodes = dict()
		self.AllEdges = list()

	def addNode(self, index, op):
		if self.AllNodes.get(index) != None:
			return self.AllNodes.get(index)
		nNew = DFGNode(index, op, self.getDelay(op))
		self.AllNodes[index] = nNew
		return nNew

	def addEdge(self, n1, n2):
		pn1 = self.AllNodes[n1]
		pn2 = self.AllNodes[n2]
		eNew = DFGEdge(pn1, pn2)
		self.AllEdges.append(eNew)
		pn1.oEdges.append(eNew)
		pn2.iEdges.append(eNew)
		return eNew

	def getDelay(self, op):
		if op == '+':
			return 1
		elif op == '*':
			return 2
		elif op == 'd':
			return self.T0
		else:
			return 0


# node of inequality graph
class IGNode:

	def __init__(self, index):
		self.index = index
		self.iEdges = list()
		self.oEdges = list()
		self.mob = [-float('inf'), float('inf')]

	def updateMob(self, minT = -float('inf'), maxT = float('inf')):
		flag = False
		if minT > self.mob[0]:
			self.mob[0] = minT
			flag = True
		if maxT < self.mob[1]:
			self.mob[1] = maxT
			flag = True
		return flag


# edge of inequality graph
class IGEdge:

	def __init__(self, pn1, pn2, delay):
		self.delay = delay
		self.nodes = (pn1, pn2)


# inequality graph
class InequalityGraph:

	def __init__(self, T0):
		self.T0 = T0
		self.AllNodes = dict()
		self.AllEdges = list()

	def addNode(self, index):
		if self.AllNodes.get(index) != None:
			return self.AllNodes.get(index)
		nNew = IGNode(index)
		self.AllNodes[index] = nNew
		return nNew

	def addEdge(self, n1, n2, delay):
		pn1 = self.addNode(n1)
		pn2 = self.addNode(n2)
		eNew = IGEdge(pn1, pn2, delay)
		self.AllEdges.append(eNew)
		pn1.oEdges.append(eNew)
		pn2.iEdges.append(eNew)
		return eNew

	def showEdges(self):
		for pe in self.AllEdges:
			print((pe.nodes[0].index, pe.nodes[1].index), pe.delay)

	def showNodes(self):
		for pn in self.AllNodes.values():
			print(f'mobility of #{pn.index} = {pn.mob}')

	def showSchedule(self):
		for pn in self.AllNodes.values():
			print(f'schedule operation #{pn.index} at time {pn.mob[0]}')


class ICGNode:

	def __init__(self, index, colors):
		self.index = index
		self.colors = colors
		self.icNodes = list()


class IncompatibilityGraph:

	def __init__(self, indexList):
		self.AllNodes = dict()
		for index in indexList:
			self.AllNodes[index] = ICGNode(index, list(range(len(indexList))))
		self.colorUsed = [False] * len(indexList)

	def assign(self):
		for pn in self.AllNodes.values():
			pn.colors = pn.colors[0]
			for neighbor in pn.icNodes:
				if type(neighbor.colors) == type(0):
					continue
				if pn.colors in neighbor.colors:
					neighbor.colors.remove(pn.colors)
			self.colorUsed[pn.colors] = True

	def showNodes(self):
		for pn in self.AllNodes.values():
			print(f'assign operation #{pn.index} to FU #{pn.colors}')
