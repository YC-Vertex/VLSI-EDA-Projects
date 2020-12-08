''' graph data structure definition '''

# node data structure
class Node:
    def __init__(self, nIndex, edges = []):
        self.index = nIndex
        self.edges = edges[:]
        self.netType = 'np' # undetermined net type
        self.visited = False
    def IsInNet(self, netType):
        return (netType in self.netType)
        
# edge data structure
class Edge:
    def __init__(self, SPTree, nodes):
        self.SPTree = SPTree
        self.nodes = nodes[:]
        self.netType = 'np' # undetermined net type
        self.deleted = False
    def IsInNet(self, netType):
        return (netType in self.netType)
    def ShowExpr(self):
        if (self.netType == 'n'):
            print('NOT(')
            self.SPTree.ShowExpr()
            print(')')
        else:
            self.SPTree.ShowExpr()
            print()

# graph data structure
class Graph:
    def __init__(self):
        self.AllNodes = dict()
        self.AllEdges = list()
        self.nNodes = list()
        self.pNodes = list()
    def ResetNodeStatus(self, status = False):
        for pn in self.AllNodes.values():
            pn.visited = status
    def ResetEdgeStatus(self, status = False):
        for pe in self.AllEdges:
            pe.deleted = status

# series-parallel node data structure
class SPNode:
    def __init__(self, signal, isLeaf = True, child = [None, None]):
        self.signal = signal
        self.isLeaf = isLeaf
        self.child = child[:]
    def ShowExpr(self):
        if self.isLeaf:
            print(self.signal, end = '')
        else:
            if self.signal == 's':
                print('AND(', end = '')
            elif self.signal == 'p':
                print('OR(', end = '')
            else:
                print(self.signal + '(', end = '')
            self.child[0].ShowExpr()
            print(',', end = '')
            self.child[1].ShowExpr()
            print(')', end = '')

def GetConnNode(pn, pe):
    if pe.nodes[0] == pn and pe.nodes[1] != pn:
        return pe.nodes[1]
    elif pe.nodes[1] == pn and pe.nodes[0] != pn:
        return pe.nodes[0]
    else:
        return None

def GetAdjNodes(pn, netType = '', noRep = True):
    adj = []
    for pe in pn.edges:
        if pe.deleted:
            continue
        pn1 = GetConnNode(pn, pe)
        if pn1.IsInNet(netType):
            adj.append(pn1)
    if noRep:
        return list(set(adj))
    else:
        return adj
