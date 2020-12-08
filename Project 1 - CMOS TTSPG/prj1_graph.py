''' graph data structure definition '''

# node data structure
class Node:
    def __init__(self, nIndex, edges = []):
        self.index = nIndex
        self.edges = edges
        self.netType = 'np' # undetermined net type
        self.visited = False
    def IsInNet(self, netType):
        return (netType in self.netType)
        
# edge data structure
class Edge:
    def __init__(self, SPTree, nodes):
        self.SPTree = SPTree
        self.nodes = nodes 
        self.netType = 'np' # undetermined net type
        self.deleted = False
    def IsInNet(self, netType):
        return (netType in self.netType)
    def ShowExpr(self):
        print(self.SPTree.ShowExpr())

# graph data structure
class Graph:
    def __init__(self):
        self.AllNodes = dict()
        self.AllEdges = list()
        self.nNodes = list()
        self.pNodes = list()

# series-parallel node data structure
class SPNode:
    def __init__(self, signal, isLeaf = True, child = [None, None]):
        self.signal = signal
        self.isLeaf = isLeaf
        self.child = child
    def ShowExpr(self):
        if self.isLeaf:
            print(self.signal, end='')
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

def GetAdjNodes(pn, netType = '', noRep = True):
    adj = []
    for pe in pn.edges:
        if pe.nodes[0] == pn and IsInNet(pe.nodes[1], netType):
            adj.append(pe.nodes[1])
        elif pe.nodes[1] == pn and IsInNet(pe.nodes[0], netType):
            adj.append(pe.nodes[0])
    if noRep:
        return list(set(adj))
    else:
        return adj
