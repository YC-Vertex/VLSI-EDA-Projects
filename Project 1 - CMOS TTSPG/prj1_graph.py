''' graph data structure definition '''

# node data structure
class Node:
    def __init__(self, nIndex, edges = []):
        self.index = nIndex
        self.edges = edges
        self.netType = 'np' # undetermined net type
    def IsInNet(self, netType):
        return (netType in self.netType)
        
# edge data structure
class Edge:
    def __init__(self, signal, pn1, pn2):
        self.signal = signal
        self.nodes = [pn1, pn2]
        self.netType = 'np' # undetermined net type
    def IsInNet(self, netType):
        return (netType in self.netType)

# graph data structure
class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = []
    def AddNode(self, nIndex, edges = []):
        nNew = Node(nIndex, edges)
        self.nodes[nIndex] = nNew
    def AddEdge_NodePtr(self, signal, pn1, pn2):
        eNew = Edge(signal, pn1, pn2)
        self.edges.append(eNew)
        pn1.edges.append(eNew)
        pn2.edges.append(eNew)
    def AddEdge_NodeIndex(self, signal, n1, n2):
        pn1 = self.nodes.get(n1)
        pn2 = self.nodes.get(n2)
        self.AddEdge_NodePtr(self, signal, pn1, pn2)
    def GetAdjNodes(self, pn, netType = ''):
        adj = []
        for pe in pn.edges:
            if pe.nodes[0] == pn and IsInNet(pe.nodes[1], netType):
                adj.append(pe.nodes[1])
            elif pe.nodes[1] == pn and IsInNet(pe.nodes[0], netType):
                adj.append(pe.nodes[0])
        return adj
        
# series-parallel node data structure
def SPNode:
    def __init__(self, sptype = ''):
        self.type = sptype
        self.child = [None, None]
